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
    #TASK = "Get me the weather of the popular city in india"
    COMPLEX_TASK = """
I'm planning a trip to the most popular city in India.
Can you help me with planing a travel by writing todos. Some of areas to look out for
1. which city is most popular
2. Current Weather there
3. Top attractions to visit

and few other details at your disposal
"""
    result = agent.invoke(
        {
            "messages": [{
                "role": "user",
                "content": COMPLEX_TASK
            }]
        }
    )
    print(result)