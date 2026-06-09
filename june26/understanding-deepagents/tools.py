from langchain.tools import tool

@tool(parse_docstring=True)
def get_weather(city:str) -> str:
    """Get the current weather for a city

    Args:
        city (str): city

    Returns:
        str: Current weather of the city
    """
    return f"It's a sunny day in {city}"

@tool(parse_docstring=True)
def get_popular_city(country:str) -> str:
    """Get the most popular city in the country

    Args:
        country (str): country

    Returns:
        str: most popular city in the country
    """
    return "Hyderabad"

@tool(parse_docstring=True)
def get_top_attractions(city: str) -> str:
    """Get top attractions of a city

    Args:
        city (str): city

    Returns:
        str: Atrractions if found else No attractions found
    """
    attractions = {
        "Hyderabad": "Charminar, Golconda Fort, Hussain Sagar Lake, Birla Mandir"
    }
    return attractions.get(city, f"No attractions found in {city}")


@tool(parse_docstring=True)
def best_time_to_visit(city: str) -> str:
    """Get the best season to visit a city

    Args:
        city (str): City

    Returns:
        str: best season to visit
    """
    seasons = {
        "Hyderabad": "October to February - mild and dry"
    }
    return seasons.get(city, f"No seasons data found for {city}")

@tool(parse_docstring=True)
def get_local_cuisine(city:str) -> str:
    """Get famous local food of a city

    Args:
        city (str): city

    Returns:
        str: famous local food
    """
    food = {
        "Hyderabad": "Biryani, Haleem, Irani Chai"
    }
    return food.get(city, f"No cuisine data found for {city}")