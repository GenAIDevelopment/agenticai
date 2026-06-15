from deepagents import create_deep_agent
from utils import get_model
from langchain.agents.middleware import PIIMiddleware


model=get_model()

agent=create_deep_agent(
    model=model,
    system_prompt="You are a fake credit card offers provider for testing",
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ]
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "i am prasanth my mail is kandutoeje@gmail.com I have a visacard 4875-2457-6547-2458 it is belongs to icici Rupay card. can you provide best offers on this card"
        }
    ]
})

print(result["messages"])

