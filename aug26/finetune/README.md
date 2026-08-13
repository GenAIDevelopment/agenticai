# Pizza Palace — Qwen3-4B Fine-tuning Bundle

A classroom-ready package for teaching QLoRA fine-tuning with Unsloth, ending in an
Ollama-deployable support agent.

## Contents

| File | What it is |
|------|------------|
| `Qwen3_PizzaPalace_finetune.ipynb` | The Colab notebook: load Qwen3-4B → QLoRA → train → export to GGUF (Ollama) + merged-16bit (vLLM) |
| `Qwen3_PizzaPalace_finetune.md` | Same notebook rendered as readable/publishable markdown |
| `pizza_palace_400.jsonl` | Full 400-record dataset (system menu / user / assistant) |
| `pizza_palace_400_train.jsonl` | Training split (352 records) |
| `pizza_palace_400_val.jsonl` | Validation split (48 records) — for watching train-vs-val loss |
| `pizza_palace_varied_seed.jsonl` | 42 hand-authored high-variety records (the gold seed) |
| `Modelfile` | Ollama Modelfile for the fine-tuned GGUF |

## Quick start

### 1. Fine-tune (Google Colab)
- Open `Qwen3_PizzaPalace_finetune.ipynb` in Colab.
- Runtime → change runtime type → **T4 GPU**.
- Upload `pizza_palace_400_train.jsonl` and `pizza_palace_400_val.jsonl`.
- Run all cells. The GGUF export lands in `pizza_gguf/`.

### 2. Deploy to Ollama
Download the `pizza_gguf/` folder from Colab, put this `Modelfile` next to it, then:

```bash
ollama create pizza-palace -f Modelfile
ollama run pizza-palace "hey do you have veg options?"
```

> The `Modelfile` assumes the GGUF is at `./pizza_gguf/unsloth.Q4_K_M.gguf`.
> If your quant or path differs, edit the `FROM` line.

## Teaching notes
- **Persona in weights, facts in the prompt.** The `SYSTEM` line bakes in the Pizza
  Palace voice; a live menu should be injected per-request (RAG) and will override it.
- **Watch the curves.** The val split exists so students see training vs. validation
  loss diverge — the overfitting fingerprint. With ~352 rows, keep to 2–3 epochs.
- **Two serving targets, one fine-tune.** GGUF/Ollama for edge; merged-16bit/vLLM for
  GPU throughput. Training format and serving format are separate decisions.
