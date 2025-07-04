from TodoApp.routers.test.utils import *
from TodoApp.routers.users import get_current_user,get_db
from fastapi import status


app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user


def test_return_user(test_user):
    response=client.get("/user")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()['username'] == 'chaithanyabikkitest'
    assert response.json()['email'] == 'chaithutest@gmail.com'
    assert response.json()['first_name'] == 'chaithanya'
    assert response.json()['last_name'] == 'bikki'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '9392125016'


def test_change_password_success(test_user):
    response=client.put("/user/password", json={"password":'testchaithu123', 'new_password':'newpassword'})

    assert response.status_code==status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response=client.put("/user/password", json={'password':'wrongpassword','new_password':'newpassword'})

    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error on changing password'}

def test_change_phone_number_success(test_user):
    response=client.put('/user/phonenumber/134432')

    assert response.status_code == status.HTTP_204_NO_CONTENT