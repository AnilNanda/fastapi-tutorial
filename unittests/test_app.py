# This file contains basics of app testing using Pytest

from app.apptest import add, sub, BankAccount, InsufficientFund
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

#Using parameter and fixture together
@pytest.mark.parametrize("deposited, withdrew, balance",[
 (200,100,100),
 (30,15,15),
 (243,124,119)
])
def test_transaction(zero_bank_account,deposited,withdrew,balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == balance

#Checking for exceptions from the code which are expected
def test_insufficient_fund(zero_bank_account):
    with pytest.raises(InsufficientFund):
        zero_bank_account.withdraw(10)