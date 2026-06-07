def is_prime(number: int) -> bool:

    # 2 is the only even prime number
    if number == 2:
        return True

    # Eliminate even numbers
    if number % 2 == 0:
        return False

    # Check divisibility up to sqrt(number)
    i = 3
    while i * i <= number:
        if number % i == 0:
            return False
        i += 2

    return True


print(is_prime(-7))
