import pytest


def test_equal_or_not_equal():
    assert 3==3
    assert 3!=1

def test_is_instance():
    assert isinstance('this is a string',str)
    assert not isinstance('10',int)

def test_boolean():
    validate=True
    assert validate is True
    assert ('hello'=='world') is False

def test_type():
    assert type('world' is str)
    assert type('hello' is not int)

def test_greate_and_less_than():
    assert 7>3 
    assert 4<10

def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert  not any(any_list)

class Student:
    def __init__(self,first_name:str, last_name:str, major:str, years:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.years=years
    
@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'ComputerScience', 3)
    

def test_student_initialization(default_employee):
    assert default_employee.first_name == 'John', 'First name Should be John'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'
    assert default_employee.major == 'ComputerScience' 
    assert default_employee.years == 3