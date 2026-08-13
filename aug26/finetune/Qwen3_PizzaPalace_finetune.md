# Pizza Palace — Fine-tuning Qwen3-4B with Unsloth (QLoRA)
### From dataset → training → GGUF (Ollama) + merged 16-bit (vLLM)

**Runtime:** Colab → change runtime type → **T4 GPU** (free tier is enough for a 4B model with QLoRA).

This notebook does five things:
1. Install Unsloth and load **Qwen3-4B** in 4-bit (QLoRA).
2. Attach LoRA adapters (the tiny trainable side-matrices).
3. Load your `pizza_palace_400_train.jsonl` / `_val.jsonl` and apply Qwen3's chat template.
4. Train, watching **train vs. validation loss**.
5. Export to **GGUF for Ollama** and **merged 16-bit for vLLM**.

> Mental model recap: the base model stays **frozen**. We only train small LoRA matrices (rank `r`), scaled by `alpha`. QLoRA means the frozen base is quantized to 4-bit so it fits in a T4's ~15 GB.

## 1. Install
Unsloth pins compatible versions of transformers/trl/peft for you. Pin Unsloth itself if you want reproducibility across class sessions — APIs move fast.

```python
# %%capture
!pip install -U unsloth unsloth_zoo
# If a class needs a frozen, reproducible setup, pin instead, e.g.:
# !pip install "unsloth==2026.5.*" "unsloth_zoo==2026.5.*"
```

## 2. Load Qwen3-4B in 4-bit

- `max_seq_length = 1024`: our records carry a system menu, so they run a little longer than a bare prompt. 1024 is comfortable headroom.
- `load_in_4bit = True`: this is the **Q** in QLoRA — the frozen base is stored in 4-bit, cutting VRAM to ~a quarter.
- `dtype = None`: let Unsloth pick (bfloat16 on newer GPUs, float16 on T4).

```python
from unsloth import FastLanguageModel
import torch

max_seq_length = 1024
dtype = None            # auto: bf16 where supported, else fp16
load_in_4bit = True     # QLoRA — 4-bit frozen base

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name    = "unsloth/Qwen3-4B",   # Unsloth's 4-bit-ready Qwen3-4B
    max_seq_length = max_seq_length,
    dtype          = dtype,
    load_in_4bit   = load_in_4bit,
    # full_finetuning = False,   # default; we're doing LoRA
)
```

## 3. Attach LoRA adapters

This is where the trainable parameters come from. Everything else stays frozen.

- **`r` (rank) = 16** — capacity of the side-matrices. 8 is fine for pure style; 16 gives a little more room for the persona + "use the provided menu" behaviour. Bigger = more capacity + more params.
- **`lora_alpha` = 16** — the scaling on the LoRA update. A common rule is alpha ≈ rank (some use 2×rank). The **alpha/rank ratio** sets the real strength.
- **`target_modules`** — which weight matrices get adapters. We hit both attention (`q,k,v,o`) and the feed-forward (`gate,up,down`) projections — the standard "all-linear" LoRA that gives the best quality.
- **`use_gradient_checkpointing = "unsloth"`** — trades a little compute for a lot of memory, so longer context fits on a T4.

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0,          # 0 is optimized in Unsloth
    bias = "none",             # optimized
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,        # try True later: scales alpha by 1/sqrt(r)
    loftq_config = None,
)
```

## 4. Bring in your dataset

Upload `pizza_palace_400_train.jsonl` and `pizza_palace_400_val.jsonl` (left sidebar → Files → upload), or pull them from Google Drive / HF. Each line is already in the `messages` format:

```json
{"messages":[{"role":"system","content":"...menu..."},
             {"role":"user","content":"veg pizza?"},
             {"role":"assistant","content":"Hey there, welcome to Pizza Palace! ..."}]}
```

```python
from datasets import load_dataset

train_dataset = load_dataset("json", data_files="pizza_palace_400_train.jsonl", split="train")
val_dataset   = load_dataset("json", data_files="pizza_palace_400_val.jsonl",   split="train")

print(train_dataset)
print("example:", train_dataset[0]["messages"][1])   # a user turn
```

### Apply Qwen3's chat template

Qwen3 uses **ChatML** under the hood (`<|im_start|>` / `<|im_end|>`). You don't write those tokens — you hand Unsloth the clean `messages` list and let `get_chat_template` + `apply_chat_template` wrap each conversation into the exact string Qwen3 was trained on.

`enable_thinking=False` keeps the empty `<think></think>` block out of training targets — for a support-agent persona we want direct replies, not reasoning traces.

```python
from unsloth.chat_templates import get_chat_template

tokenizer = get_chat_template(tokenizer, chat_template="qwen3")   # or "qwen-2.5" on older Unsloth

def format_chat(examples):
    texts = [
        tokenizer.apply_chat_template(
            convo, tokenize=False, add_generation_prompt=False,
            enable_thinking=False,
        )
        for convo in examples["messages"]
    ]
    return {"text": texts}

train_dataset = train_dataset.map(format_chat, batched=True)
val_dataset   = val_dataset.map(format_chat,   batched=True)

print(train_dataset[0]["text"][:600])
```

## 5. Trainer configuration

Every hyperparameter here maps to something we discussed:

- **`learning_rate = 2e-4`** — step size per weight update. LoRA's sweet spot. Loss jittering → lower it; barely moving → raise it.
- **`per_device_train_batch_size = 2` × `gradient_accumulation_steps = 4`** → **effective batch size 8**. The T4 can't hold 8 at once, so we accumulate 4 micro-batches of 2 and apply one combined update — big-batch stability, small-batch memory.
- **`num_train_epochs = 3`** — with ~352 rows, 2–3 passes is the sweet spot; more risks memorizing.
- **`eval_strategy = "steps"`** — this is what lets you *watch* train vs. val loss diverge (the overfitting fingerprint).
- **`warmup_steps`** — ramp the LR up gently so early updates don't thrash the weights.

```python
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = train_dataset,
    eval_dataset = val_dataset,
    args = SFTConfig(
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,     # effective batch = 8
        warmup_steps = 5,
        num_train_epochs = 3,
        learning_rate = 2e-4,
        logging_steps = 5,
        eval_strategy = "steps",
        eval_steps = 20,                     # check val loss every 20 steps
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",
    ),
)
```

### Train only on the assistant's replies

Crucial for instruction tuning: we don't want the model spending capacity learning to *predict the customer's message or the menu*. `train_on_responses_only` masks the loss so gradients flow **only** from the assistant turns. For Qwen3/ChatML the turn markers are `<|im_start|>user\n` and `<|im_start|>assistant\n`.

```python
from unsloth.chat_templates import train_on_responses_only

trainer = train_on_responses_only(
    trainer,
    instruction_part = "<|im_start|>user\n",
    response_part    = "<|im_start|>assistant\n",
)
```

### Go

```python
trainer_stats = trainer.train()
```

### Read the curves
Pull the logged history and plot **training vs. validation loss**. Healthy = both descend and stay close. The moment val flattens/rises while train keeps dropping → overfitting → stop or reduce epochs/rank. Great live demo for the class.

```python
import matplotlib.pyplot as plt

hist = trainer.state.log_history
tr = [(h["step"], h["loss"])      for h in hist if "loss" in h]
ev = [(h["step"], h["eval_loss"]) for h in hist if "eval_loss" in h]

plt.figure(figsize=(8,5))
if tr: plt.plot(*zip(*tr), label="training loss")
if ev: plt.plot(*zip(*ev), label="validation loss", marker="o")
plt.xlabel("step"); plt.ylabel("loss"); plt.legend(); plt.title("Pizza Palace fine-tune"); plt.grid(True, alpha=.3)
plt.show()
```

## 6. Quick sanity test (before export)
Switch to fast inference and talk to the model. Does it sound like Pizza Palace?

```python
FastLanguageModel.for_inference(model)

messages = [
    {"role": "system", "content": "You are a warm, upbeat Pizza Palace support agent. Today's menu:\nMargherita ₹210\nPaneer Supreme ₹330\nGarlic Breadsticks ₹120\nCola ₹60\nUse ONLY this menu."},
    {"role": "user", "content": "hey do u have anything veg"},
]
inputs = tokenizer.apply_chat_template(
    messages, tokenize=True, add_generation_prompt=True,
    return_tensors="pt", enable_thinking=False,
).to("cuda")

out = model.generate(input_ids=inputs, max_new_tokens=128, temperature=0.7, top_p=0.9)
print(tokenizer.decode(out[0], skip_special_tokens=True))
```

## 7. Save the LoRA adapters (lightweight checkpoint)
Just the adapters — a few MB. Useful to keep, and to re-merge later without retraining.

```python
model.save_pretrained("pizza_lora")          # local
tokenizer.save_pretrained("pizza_lora")
# model.push_to_hub("your-username/pizza-qwen3-lora", token="hf_...")   # optional
```

## 8. Export → GGUF for **Ollama**

`save_pretrained_gguf` merges the LoRA into the base, converts to GGUF via llama.cpp, and quantizes. Pick a quant:
- **`q4_k_m`** — best size/quality trade-off, the usual choice for laptops/edge.
- **`q8_0`** — larger, higher fidelity.
- **`f16`** — full precision GGUF (biggest).

This step compiles llama.cpp the first time, so give it a few minutes.

```python
model.save_pretrained_gguf(
    "pizza_gguf",
    tokenizer,
    quantization_method = "q4_k_m",   # try "q8_0" for higher fidelity
)
# Produces e.g. pizza_gguf/unsloth.Q4_K_M.gguf
!ls -lh pizza_gguf
```

### Run it in Ollama
Unsloth writes a `Modelfile` next to the GGUF with the correct Qwen3 chat template baked in. Two ways to use it:

**A) On a machine with Ollama installed** (your GCP L4 VM, or locally): download the `.gguf` + `Modelfile`, then:
```bash
ollama create pizza-palace -f Modelfile
ollama run pizza-palace
```

**B) Inside Colab** (to demo end-to-end):

```python
# Install + start Ollama inside Colab (demo only)
!curl -fsSL https://ollama.com/install.sh | sh
import subprocess, time
subprocess.Popen(["ollama", "serve"])
time.sleep(5)

# Unsloth auto-generates a Modelfile; if you need one manually, this works too:
modelfile = '''FROM ./pizza_gguf/unsloth.Q4_K_M.gguf
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
"""
PARAMETER stop "<|im_end|>"
PARAMETER temperature 0.7
'''
open("pizza_gguf/Modelfile", "w").write(modelfile)

!cd pizza_gguf && ollama create pizza-palace -f Modelfile
!ollama run pizza-palace "hey do you have veg pizza?"
```

## 9. Export → merged 16-bit for **vLLM**

vLLM serves standard HF safetensors, **not** GGUF. So we merge the LoRA into the base at 16-bit precision with `save_method="merged_16bit"`. (`merged_4bit` also exists if you want a smaller, lower-fidelity artifact.)

```python
model.save_pretrained_merged(
    "pizza_merged_16bit",
    tokenizer,
    save_method = "merged_16bit",
)
!ls -lh pizza_merged_16bit
# Optional straight-to-Hub:
# model.push_to_hub_merged("your-username/pizza-qwen3", tokenizer, save_method="merged_16bit", token="hf_...")
```

### Serve with vLLM
On your GPU box (L4/A100), point vLLM at the merged folder:
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/pizza_merged_16bit \
    --served-model-name pizza-palace \
    --max-model-len 1024
```
Then it speaks the OpenAI API:
```bash
curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "pizza-palace",
  "messages": [
    {"role":"system","content":"You are a Pizza Palace agent. Menu: Margherita ₹210, Cola ₹60. Use only this menu."},
    {"role":"user","content":"veg options?"}
  ]
}'
```

## 10. Get your files out of Colab
Zip and download, or push to Drive.

```python
from google.colab import files
!zip -r pizza_gguf.zip pizza_gguf
!zip -r pizza_merged_16bit.zip pizza_merged_16bit
files.download("pizza_gguf.zip")
# files.download("pizza_merged_16bit.zip")   # large — Drive is usually better
```

---
### Recap: which artifact for what
| Target | Method | Output | Serve with |
|---|---|---|---|
| **Ollama / laptop / edge** | `save_pretrained_gguf(..., "q4_k_m")` | `.gguf` + `Modelfile` | `ollama create` / `ollama run` |
| **vLLM / GPU serving** | `save_pretrained_merged(..., "merged_16bit")` | HF safetensors folder | `vllm ... --model <folder>` |
| **Re-use / re-merge later** | `save_pretrained("pizza_lora")` | LoRA adapters (MB) | reload + merge |

**Teaching note:** GGUF is quantized-for-CPU/edge; the vLLM path stays 16-bit for GPU throughput. Same fine-tune, two deployment targets — a clean way to show students that *training* and *serving format* are separate decisions.
