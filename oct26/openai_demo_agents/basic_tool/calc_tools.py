from agents import function_tool


@function_tool
def add(a: int | float, b: int | float) -> int | float:
    """Adds two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        int | float: The sum of the two numbers.
    """
    result = a + b
    print(f"[TOOL] add({a}, {b}) => {result}")
    return result


@function_tool
def sub(a: int | float, b: int | float) -> int | float:
    """Subtracts the second number from the first number.

    Args:
        a: The number from which to subtract.
        b: The number to subtract.

    Returns:
        int | float: The difference between the two numbers.
    """
    result = a - b
    print(f"[TOOL] sub({a}, {b}) => {result}")
    return result


@function_tool
def mul(a: int | float, b: int | float) -> int | float:
    """Multiplies two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        int | float: The product of the two numbers.
    """
    result = a * b
    print(f"[TOOL] mul({a}, {b}) => {result}")
    return result


@function_tool
def div(a: int | float, b: int | float) -> float:
    """Divides the first number by the second number.

    Args:
        a: The dividend.
        b: The divisor. Must not be zero.

    Returns:
        float: The quotient of the division.

    Raises:
        ValueError: If the divisor is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")

    result = a / b
    print(f"[TOOL] div({a}, {b}) => {result}")
    return result


@function_tool
def modulus(a: int | float, b: int | float) -> int | float:
    """Returns the remainder after dividing the first number by the second.

    Args:
        a: The dividend.
        b: The divisor. Must not be zero.

    Returns:
        int | float: The remainder of the division.

    Raises:
        ValueError: If the divisor is zero.
    """
    if b == 0:
        raise ValueError("Modulus by zero is not allowed.")

    result = a % b
    print(f"[TOOL] modulus({a}, {b}) => {result}")
    return result