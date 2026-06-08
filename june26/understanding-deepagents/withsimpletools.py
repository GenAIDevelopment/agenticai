from utils import get_model
from langchain.tools import tool
from deepagents import create_deep_agent


@tool()
def add(a:int|float, b:int|float) -> int | float:
    """Performs addition of two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int | float: sum of two numbers
    """
    return a + b

@tool()
def subtract(a: int | float, b: int | float) -> int | float:
    """Performs subtraction of two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int | float: difference of two numbers
    """
    return a - b


@tool()
def multiply(a: int | float, b: int | float) -> int | float:
    """Performs multiplication of two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        int | float: product of two numbers
    """
    return a * b


@tool()
def divide(a: int | float, b: int | float) -> float:
    """Performs division of two numbers

    Args:
        a (int | float): number
        b (int | float): number

    Returns:
        float: quotient of two numbers

    Raises:
        ValueError: if b is zero
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


@tool()
def modulus(a: int, b: int) -> int:
    """Performs modulus operation on two numbers

    Args:
        a (int): number
        b (int): number

    Returns:
        int: remainder after division

    Raises:
        ValueError: if b is zero
    """
    if b == 0:
        raise ValueError("Modulus by zero is not allowed")
    return a % b


model = get_model()

agent = create_deep_agent(
    model=model,
    system_prompt="You are an helpful assistant in performing logical and mathematical operations",
    tools=[add, subtract, multiply, divide, modulus]
)

