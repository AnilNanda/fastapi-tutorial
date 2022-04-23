from app.apptest import add, sub


def test_add():
    print("hello")
    assert add(7,3) == 10

def test_sub():
    assert sub(8,3) == 5