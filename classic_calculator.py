# Classic Calculator

def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        print("You cannot divide by 0.")
        return None  # Return None to indicate an error
    else:
        return x / y


def exponent(x, y):
    return x ** y


def main():
    # User input with error handling
    try:
        x_input = int(input("X: "))
        y_input = int(input("Y: "))
    except ValueError:
        print("Please enter valid integer numbers for X and Y.")
        return  # Exit the function if the input is invalid

    # Displaying menu
    print("=" * 35)
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exponentiation")
    print("=" * 35)

    try:
        user_input = int(input("Please choose an operation: "))
    except ValueError:
        print("Please enter a valid integer for the operation.")
        return

    result = None

    if user_input == 1:
        result = add(x_input, y_input)
    elif user_input == 2:
        result = subtract(x_input, y_input)
    elif user_input == 3:
        result = multiply(x_input, y_input)
    elif user_input == 4:
        result = divide(x_input, y_input)
    elif user_input == 5:
        result = exponent(x_input, y_input)
    else:
        print("Invalid operation.")

    # Print the result if it is valid
    if result is not None:
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
