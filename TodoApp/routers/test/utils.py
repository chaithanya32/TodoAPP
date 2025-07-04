from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker


from TodoApp.database import Base 
from TodoApp.main import app
from fastapi.testclient import TestClient
from fastapi import status

from TodoApp.models import Todos, Users
from TodoApp.routers.auth import bcrypt_context 
import pytest


SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)

TestingSessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return{'username':'chaithanya', 'id':1, 'user_role':'admin'}


client=TestClient(app)

@pytest.fixture
def test_todo():
    todo=Todos(
        title="Learn to code!",
        description='Need to learn Everyday',
        priority=5,
        complete=False,
        owner_id=1,
    
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user=Users(
        username="chaithanyabikkitest",
        email="chaithutest@gmail.com",
        first_name="chaithanya",
        last_name="bikki",
        hashed_password=bcrypt_context.hash("testchaithu123"),
        role='admin',
        phone_number=9392125016
    )

    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()



