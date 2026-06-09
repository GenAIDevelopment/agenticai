from utils import get_model
from tools import (
    get_local_cuisine,
    best_time_to_visit,
    get_popular_city,
    get_top_attractions,
    get_weather
)
from deepagents import create_deep_agent

model = get_model()

agent = create_deep_agent(
    model=model,
    tools=[
        get_weather,
        get_local_cuisine,
        best_time_to_visit,
        get_popular_city,
        get_top_attractions
    ],
    system_prompt="You are a helpful travel assistant for India"
)

if __name__ == "__main__":
    TASK = "Get me the weather of the popular city in india"
    result = agent.invoke(
        {
            "messages": [{
                "role": "user",
                "content": TASK
            }]
        }
    )
    print(result)