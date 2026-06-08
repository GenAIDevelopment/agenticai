from deepagents import create_deep_agent
from utils import get_model

model = get_model()

agent = create_deep_agent(
    model=model,
    system_prompt="You are a research assistant"
)
