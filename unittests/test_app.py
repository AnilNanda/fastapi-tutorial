from app.apptest import add, sub, BankAccount
import pytest

@pytest.mark.parametrize("num1,num2,expected",[
    (3,4,7),
    (12,17,29),
    (41,54,95)
])
def test_add(num1, num2, expected):
    print("hello")
    assert add(num1,num2) == expected

def test_sub():
    assert sub(8,3) == 5


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

#The fixture function is passed as parameter to testing function and same name is referred as return object
def test_starting_balance(bank_account): 
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert  zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit():
    bankaccount = BankAccount(50)
    bankaccount.deposit(20)
    assert bankaccount.balance == 70

def test_collect_interest():
    bankaccount = BankAccount(50)
    bankaccount.collect_interest()
    assert round(bankaccount.balance,6) == 55