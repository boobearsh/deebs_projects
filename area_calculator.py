import math

print("==================")
print("Area Calculator 📐")
print("==================")
print(" ")

print("1) Triangle")
print("2) Rectangle")
print("3) Square")
print("4) Circle")
print("5) Quit")
print(" ")

try:
    shape_input = int(input("Which shape: "))
except ValueError:
    print("Error: Please select a valid number")
    exit()

# Handling Quit option early
if shape_input == 5:
    print("Exiting the program. Goodbye!")
    exit()

if shape_input not in [1, 2, 3, 4]:
    print("Error: Please select a valid option (1-5).")
    exit()

if shape_input == 1:  # Triangle
    try:
        base_input = float(input("Base: "))
        height_input = float(input("Height: "))
    except ValueError:
        print("Error: Please enter valid numbers for base and height.")
        exit()
    area = (base_input * height_input) / 2
    print(f"The area is {area}")

elif shape_input == 2:  # Rectangle
    try:
        length_input = float(input("Length: "))
        width_input = float(input("Width: "))
    except ValueError:
        print("Error: Please enter valid numbers for length and width.")
        exit()
    area = length_input * width_input
    print(f"The area is {area}")

elif shape_input == 3:  # Square
    try:
        side_input = float(input("Side: "))
    except ValueError:
        print("Error: Please enter a valid number for the side.")
        exit()
    area = side_input ** 2
    print(f"The area is {area}")

elif shape_input == 4:  # Circle
    try:
        radius_input = float(input("Radius: "))
    except ValueError:
        print("Error: Please enter a valid number for the radius.")
        exit()
    area = math.pi * (radius_input ** 2)
    print(f"The area is {area}")

print("Thank you for using the Area Calculator!")
