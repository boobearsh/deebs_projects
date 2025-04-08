# Define a BankAccount class.
# Then, let's use the __init__() method to set the following attributes:

# first_name (string)
# last_name (string)
# account_id (integer)
# account_type (string)
# pin (integer)
# balance (float)
# Next, let's create three methods:

# .deposit(): Add money into the account and return the new balance.
# .withdraw(): Take money out by subtracting from balance and returning the withdrawn amount.
# .display_balance(): Print the current value of balance.
# Lastly, initialize a new object from the BankAccount class and use these methods to do the following:

# Deposit $XXXX in the account.
# Withdraw $XXXX from the account.
# Print the current account balance.


# Codedex Solution:

class BankAccount:
    def __init__(self, first_name, last_name, account_id, account_type, pin, balance):
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = account_id
        self.account_type = account_type
        self.pin = pin
        self.balance = balance

    def deposit(self, deposit_amount):
        self.balance = self.balance + deposit_amount
        return self.balance

    def withdraw(self, withdraw_amount):
        self.balance = self.balance - withdraw_amount
        return self.balance

    def display_balance(self):
        print(f"${self.balance}")


checking_account = BankAccount(
    "Dave",
    "Ortega",
    123456789,
    "checking",
    0000,
    500.00)

checking_account.deposit(100)
checking_account.display_balance()
checking_account.withdraw(50)
checking_account.display_balance()
