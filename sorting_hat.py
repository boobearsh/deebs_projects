# Sorting Hat Quiz

print("Welcome to the Sorting Hat!")

house_gryffindor = 0
house_ravenclaw = 0
house_hufflepuff = 0
house_slytherin = 0

show_question1 = "Q1) Do you like Dawn or Dusk? "
option_1 = "\n   1) Dawn"
option_2 = "\n   2) Dusk"
print(show_question1, option_1, option_2)

question_1 = int(input("Answer: "))

if question_1 == 1:
    house_gryffindor += 1
    house_ravenclaw += 1
else:
    house_hufflepuff += 1
    house_slytherin += 1

show_question2 = "Q2) When I'm dead, I want people to remember as: "
option_1 = "\n   1) The Good"
option_2 = "\n   2) The Great"
option_3 = "\n   3) The Wise"
option_4 = "\n   4) The Bold"
print(show_question2, option_1, option_2, option_3, option_4)

question_2 = int(input("Answer: "))

if question_2 == 1:
    house_hufflepuff += 2
elif question_2 == 2:
    house_slytherin += 2
elif question_2 == 3:
    house_ravenclaw += 2
elif question_2 == 4:
    house_gryffindor += 2
else:
    print("Wrong input.")

show_question3 = "Q3) Which kind of instrument most pleases your ear?: "
option_1 = "\n   1) The violin"
option_2 = "\n   2) The trumpet"
option_3 = "\n   3) The piano"
option_4 = "\n   4) The drum"
print(show_question3, option_1, option_2, option_3, option_4)

question_3 = int(input("Answer: "))

if question_3 == 1:
    house_slytherin += 4
elif question_3 == 2:
    house_hufflepuff += 4
elif question_3 == 3:
    house_ravenclaw += 4
elif question_3 == 4:
    house_gryffindor += 4
else:
    print("Wrong input.")

points_1 = house_gryffindor
points_2 = house_ravenclaw
points_3 = house_hufflepuff
points_4 = house_slytherin

print("=" * 20)

# Print the score for each house
print(f"Gryffindor: {house_gryffindor}")
print(f"Ravenclaw: {house_ravenclaw}")
print(f"Hufflepuff: {house_hufflepuff}")
print(f"Slytherin: {house_slytherin}")

print("=" * 20)

teams = {  # Dictionary, String = Who wins , value = is the points, max, of who wins
    "GRYFFINDOR WINS!": (points_1),
    "RAVENCLAW WINS!": (points_2),
    "HUFFLEPUFF WINS!": (points_3),
    "SLYTHERIN WINS!": (points_4)
}

winner = max(teams, key=teams.get)
print(winner)

print("=" * 20)
