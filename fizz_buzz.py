# Fizz Buzz Game

# For multiples of 3, print "Fizz" instead of the number.
# For multiples of 5, print "Buzz" instead of the number.
# For multiples of 3 and 5, print "FizzBuzz".

# Output, up to 100

for i in range(1, 101):  # Include 100 in the range because 99 is a multiple.
    if i % 3 == 0 and i % 5 == 0:  # Check if divisible by both 3 and 5
        print("FizzBuzz")
    elif i % 5 == 0:  # Check if divisible by 5
        print("Buzz")
    elif i % 3 == 0:  # Check if divisible by 3
        print("Fizz")
    else:
        print(i)
