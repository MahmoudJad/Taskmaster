from routers.admin import get_db, get_current_user
from models import Todos

from test.utils import TestingSessionLocal, override_get_db, override_get_current_user, client, app, test_todo

from fastapi import status




app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
            'complete': False,
            'description': 'Test Description',
            'id': 1,
            'owner_id': 1,
            'priority': 5,
            'title': 'Test Todo',
            }]
    
def test_admin_delete_todos(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/17")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}