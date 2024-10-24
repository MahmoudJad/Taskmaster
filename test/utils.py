from routers.todos import get_db, get_current_user
# from TodoApp import constant
from models import Todos, Users
from routers.auth import bcrypt_context

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient


import pytest

from database import Base
from main import app


# DATABASE_URL = (
#     "postgresql://"
#     + constant.POSTGRES_USER
#     + ":"
#     + constant.POSTGRES_PASSWORD
#     + "@"
#     + constant.POSTGRES_SERVER
#     + "/"
#     + constant.TEST_DB
# )
DATABASE_URL = "sqlite:///./testTodo.db"

engine = create_engine(DATABASE_URL, poolclass=StaticPool)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return{"username": "Jad", "id": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)



@pytest.fixture
def test_todo():
    todo = Todos(
        id=1,
        title="Test Todo", 
        description="Test Description", 
        priority=5, 
        complete=False,
        owner_id=1
        )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit() 
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = "Jad",
        email = "mahmoud@elg4ml.com",
        first_name = "Mahmoud",
        last_name = "Jad",
        hashed_password = bcrypt_context.hash("testpassword"),
        role = "admin",
        phone_number = "0100000033"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()