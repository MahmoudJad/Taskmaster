from routers.users import get_db, get_current_user
from models import Users

from test.utils import TestingSessionLocal, override_get_db, override_get_current_user, client, app, test_user

from fastapi import status



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "Jad"
    assert response.json()["email"] == "mahmoud@elg4ml.com"
    assert response.json()["first_name"] == "Mahmoud"
    assert response.json()["last_name"] == "Jad"    
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "0100000033"

def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "123456"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_change_password_failed(test_user):
    response = client.put("/user/password", json={"password": "testp@ssword", "new_password": "123456"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED    


def test_update_phone_success(test_user):
    response = client.put("/user/phone/0100000033")
    assert response.status_code == status.HTTP_204_NO_CONTENT
   


    