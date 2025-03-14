class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Kwota wpłaty musi być dodatnia.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Kwota wypłaty musi być dodatnia.")
        self.balance -= amount

    def get_balance(self):
        return self.balance

