# %%

import random

MAX_LINES = 3
MAX_BET = 100  # $100
MIN_BET = 1  # $1

ROWS = 3
COLUMNS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}


def get_slot_machine_spin(rows, columns, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for i in range(symbol_count):
            all_symbols.append(symbol)

    columns = [[], [], []]


def deposit():
    while True:
        amount = input("How much money would you like to deposit? $")
        if amount.isdigit():  # Makes sure the amount given is an integer
            amount = int(amount)
            if amount > 0:  # If the amount is more than $0, break
                break
            else:
                print("Amount must be > $0")  # If amount, is not > $0
        else:
            # If amount is > $0, returns amount
            print("Please enter an amount.")
    return amount


def get_number_of_lines():
    while True:
        lines = input("Enter the # of lines (1 - " + str(MAX_LINES) + ")? ")
        if lines.isdigit():  # Makes sure the amount is an integer
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:  # If the amount of lines between 1-3
                break
            else:
                # If amount of lines is not valid
                print("Enter a valid # of lines.")
        else:
            # If amount is > $0, returns amount
            print("Please enter a number.")
    return lines


def get_bet():
    while True:
        amount = input("How much money would you like to bet, on each line? $")
        if amount.isdigit():  # Makes sure the amount is an integer
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:  # If the bet amount is between $1 - $100
                break
            else:
                # If amount, is not > $0
                print(f"Amount bet must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            # If amount is > $0, returns amount
            print("Please enter an amount.")
    return amount


def main():  # main.py of our program, let's us run again if we want to continue playing
    balance = deposit()
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"Your balance is insufficient. Your current balance is: {balance}")
        else:
            break

    print(
        f"You are betting ${bet} on {lines} lines. Your Total bet is equal to: ${total_bet}")

    print(balance, lines)


main()
