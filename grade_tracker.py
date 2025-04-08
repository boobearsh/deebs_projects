# Grade Tracker

import csv
import math

# Features:
# 1. Add a new student record.
# 2. View all student records.
# 3. Calculate grade statistics (average, highest, lowest).
# 4. Save records to a CSV file.
# 5. Load records from a CSV file.
# 6. Bonus: Show unique grades using a set and display the first record as a tuple.
# 7. Exit the program.

student_records = []  # initialize an empty list


def main_menu():
    print("=" * 35)
    print("1. Add a new student record.")
    print("2. View all student records.")
    print("3. Calculate grade statistics (average, highest, lowest).")
    print("4. Save records to a CSV files.")
    print("5. Load records from a CSV file.")
    print("6. Bonus: Show unique grades using a set and display the first record as a tuple.")
    print("7. Exit the program.")
    print("=" * 35)


def add_student():
    name = input("Enter the student's name: ")
    age = int(input("Enter the student's age: "))
    grade = float(input("Enter the student's grades: "))

    # Create the student's record as a dictionary
    student = {"name": name, "age": age, "grade": grade}

    # Add the student to the global student record list
    student_records.append(student)
    print(f"Student {name} added successfully!")


def view_students():
    if not student_records:
        print("Student not within the records or No students within record. ")
        return

    print("Student Records: ")
    # This will loop through every student record and display it.
    for idx, student in enumerate(student_records, start=1):
        print(
            f"{idx}. Name: {student['name']}, Age: {student['age']}, Grade: {student['grade']}")


def calculate_average_grade():
    if not student_records:
        print("Student records unavailable to calculalate average statistics ")
        return

    # Sum all grades and calculate average.
    total_grade = sum(student['grade'] for student in student_records)
    count = len(student_records)
    average = total_grade / count
    highest = max(student['grade'] for student in student_records)
    lowest = min(student['grade'] for student in student_records)

    # Calculate square root of the average using the math module.
    sqrt_average = math.sqrt(average)

    # Display the statistics with formatted output.
    print(f"Average Grade: {average:.2f}")
    print(f"Highest Grade: {highest:.2f}")
    print(f"Lowest Grade: {lowest:.2f}")
    print(f"Square Root of Average Grade (for fun): {sqrt_average:.2f}")


def save_records_to_csv():
    filename = input(
        "Enter filename here: ").strip()
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'age', 'grade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the CSV header.
            for student in student_records:
                writer.writerow(student)
        print(f"Records saved to {filename} successfully! ")
    except Exception as e:
        print(f"Error saving records: {e}")


def load_records_from_csv():
    filename = input(
        "Load filename here: ").strip()
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            loaded_records = []
            for row in reader:
                # Convert 'age' and 'grade' from string to proper data types.
                student = {"name": row['name'], "age": int(
                    row['age']), "grade": float(row['grade'])}
                loaded_records.append(student)
            global student_records
            student_records = loaded_records
        print(f"Records loaded from {filename} successfully! ")
    except Exception as e:
        print(f"Error loading records: {e}")


def bonus_info():
    """
    BONUS: Demonstrate the use of sets and tuples.

    - Use a set to show unique grades.
    - Convert the first student record to a tuple.
    """
    if not student_records:
        print("No student records to display bonus info.")
        return

    # Create a set of unique grades.
    unique_grades = {student['grade'] for student in student_records}
    print(f"Unique Grades: {unique_grades}")

    # Convert the first record to a tuple for an immutable record.
    first_student = student_records[0]
    student_tuple = (first_student['name'],
                     first_student['age'], first_student['grade'])
    print(f"First Student as Tuple: {student_tuple}")


def main():
    while True:
        main_menu()
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            calculate_average_grade()
        elif choice == "4":
            save_records_to_csv()
        elif choice == "5":
            load_records_from_csv()
        elif choice == "6":
            bonus_info()
        elif choice == "7":
            print("Exiting Student Grade Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7. ")


if __name__ == "__main__":
    main()
