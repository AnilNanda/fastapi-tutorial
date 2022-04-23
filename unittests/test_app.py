from app.apptest import add, sub
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