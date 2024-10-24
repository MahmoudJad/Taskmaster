
import pytest


def test_equal_or_not():
    assert 1 == 1
    assert 1 != 2
    


def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("1", int)


def test_boolean():
    validated = True
    assert validated is True
    assert ("Hello" == "world") is False


def test_type():
    assert type(1) is int
    assert type(1.0) is float
    assert type("Hello") is str
    assert type("world") is not int
    assert type([1, 2, 3]) is list
    assert type((1, 2, 3)) is tuple
    assert type({"name": "John", "age": 30}) is dict
    assert type({1, 2, 3}) is set

def test_greater_and_less_than():
    assert 10 > 5
    assert 5 < 10
    assert 10 >= 10
    assert 10 <= 10
    assert 10 >= 5
    assert 5 <= 10
    assert 10 > 5 >= 5
    assert 5 < 10 <= 10

def test_list():
    my_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in my_list
    assert 7 not in my_list
    assert all(my_list)
    assert not any(any_list)



class Student:
    def __init__(self, first_name: str, last_name: str, major: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year 


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 2023)



def test_person_initialization(default_student):
    assert default_student.first_name == "John"
    assert default_student.last_name == "Doe"
    assert default_student.major == "Computer Science"
    assert default_student.year == 2023
