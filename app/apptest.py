
def add(a,b):
    return a+b

def sub(a,b):
    return a-b

class InsufficientFund(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFund("Insufficient fund in account")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1