
from routers.todos import get_db, get_current_user

from models import Todos

from test.utils import TestingSessionLocal, override_get_db, override_get_current_user, client, app, test_todo

from fastapi import status




app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_read_all_authenticate(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False,'description': 'Test Description','id':1, 'owner_id': 1,'priority': 5,'title': 'Test Todo'}]


def test_read_one_authenticate(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False,'description': 'Test Description','id':1, 'owner_id': 1,'priority': 5,'title': 'Test Todo'}


def test_read_one_not_found(test_todo):
    response = client.get("/todos/todo/17")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todo):
    payload = {'complete': False,'description': 'Test Description','id':1, 'owner_id': 1,'priority': 5,'title': 'Test Todo'}
    response = client.post("/todos/todo", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    # assert response.json() == {'detail': 'Todo created successfully.'}

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == payload.get("title")
    assert model.description == payload.get("description")
    assert model.priority == payload.get("priority")
    assert model.complete == payload.get("complete")
    assert model.owner_id == payload.get("owner_id")


def test_update_todo(test_todo):
    payload = {
        'title': 'Change the title and description',
        'description': 'Change the title and description',
        'priority': 5,
        'id': 1,
        'owner_id': 1,
        'complete': False,
        
    }

    response = client.put("/todos/todo/1", json=payload)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == payload.get("title")


def test_update_todo_not_found(test_todo):
    payload = {
        'title': 'Change the title and description',
        'description': 'Change the title and description',
        'priority': 5,
        'owner_id': 1,
        'complete': False,
        
    }

    response = client.put("/todos/todo/17", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
    

def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todos/todo/17")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
   
