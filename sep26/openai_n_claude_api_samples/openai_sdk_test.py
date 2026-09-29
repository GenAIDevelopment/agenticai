from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, SQLiteSession

import asyncio
import os
import random
from typing import Literal


load_dotenv()

@function_tool
def get_weather(
    city: str,
) -> Literal[
    "Sunny",
    "Clear",
    "Partly Cloudy",
    "Mostly Cloudy",
    "Overcast",
    "Humid",
    "Muggy",
    "Rain",
    "Light Rain",
    "Heavy Rain",
    "Drizzle",
    "Showers",
    "Snow",
    "Light Snow",
    "Heavy Snow",
    "Snow Flurries",
    "Sleet",
    "Ice Pellets",
    "Freezing Rain",
    "Freezing Drizzle",
    "Hail",
    "Graupel",
    "Thunderstorm",
    "Severe Thunderstorm",
    "Tropical Storm",
    "Hurricane",
    "Typhoon",
    "Cyclone",
    "Tornado",
    "Monsoon",
    "Blizzard",
    "Winter Storm",
    "Breezy",
    "Windy",
    "Gale",
    "Squall",
    "Dust Storm",
    "Haboob",
    "Sandstorm",
    "Fog",
    "Freezing Fog",
    "Mist",
    "Haze",
    "Smoke",
    "Smog",
    "Volcanic Ash",
    "Waterspout",
    "Landspout",
    "Firewhirl",
]:
    """This tool returns the weather of the city.

    Args:
        city (str): The name of the city to check the weather for.

    Returns:
        str: weather condition.
    """
    weather_conditions = [
        # Fair & Clear Conditions
        "Sunny",
        "Clear",
        "Partly Cloudy",
        "Mostly Cloudy",
        "Overcast",
        "Humid",
        "Muggy",

        # Liquid & Frozen Precipitation
        "Rain",
        "Light Rain",
        "Heavy Rain",
        "Drizzle",
        "Showers",
        "Snow",
        "Light Snow",
        "Heavy Snow",
        "Snow Flurries",
        "Sleet",
        "Ice Pellets",
        "Freezing Rain",
        "Freezing Drizzle",
        "Hail",
        "Graupel",

        # Severe & Cyclonic Weather
        "Thunderstorm",
        "Severe Thunderstorm",
        "Tropical Storm",
        "Hurricane",
        "Typhoon",
        "Cyclone",
        "Tornado",
        "Monsoon",
        "Blizzard",
        "Winter Storm",

        # Wind & Dust Phenomena
        "Breezy",
        "Windy",
        "Gale",
        "Squall",
        "Dust Storm",
        "Haboob",
        "Sandstorm",

        # Low Visibility & Atmospheric Conditions
        "Fog",
        "Freezing Fog",
        "Mist",
        "Haze",
        "Smoke",
        "Smog",
        "Volcanic Ash",

        # Rare & Vortex Phenomena
        "Waterspout",
        "Landspout",
        "Firewhirl",
    ]

    return random.choice(weather_conditions)


async def main():
    agent = Agent(
        name="Tutor",
        instructions="Explain the concept in simple terms with example",
        model="gpt-5.6-luna",
    )

    result = await Runner.run(
        agent,
        input="Explain Newtons 1st law",
    )

    print(result.final_output)

async def main_with_tools():
    agent = Agent(
        name="Guide",
        instructions="Help tourists wear the right outfit according to weather",
        model="gpt-5.6-luna",
        tools=[get_weather]
    )

    result = await Runner.run(
        agent,
        input="I'm in hyderabad what should i wear and do i need to carry umbrella",
    )

    print(result.final_output)


async def main_with_memory():
    agent = Agent(
        name="Helpful Assistant",
        instructions="you are a helpful assistant",
        model="gpt-5.6-luna",
        tools=[get_weather]
    )

    session = SQLiteSession("classroom_29_sep")
    result = await Runner.run(
            agent,
            input="I'm in hyderabad",
            session=session
        )
    #print(result.final_output)
    result = await Runner.run(
                agent,
                input="Can you tell me which city i'm in and whats the state",
                session=session
            )
    print(result.final_output)



if __name__ == "__main__":
    #asyncio.run(main())
    #asyncio.run(main_with_tools())
    asyncio.run(main_with_memory())