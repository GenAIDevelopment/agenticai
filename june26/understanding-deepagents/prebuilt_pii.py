from deepagents import create_deep_agent
from utils import get_model
from langchain.agents.middleware import PIIMiddleware

model = get_model()

agent = create_deep_agent(
    model=model,
    system_prompt="You are a research assistant",
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ]
)
