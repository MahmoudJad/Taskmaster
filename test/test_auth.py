from datetime import timedelta
from test.utils import TestingSessionLocal, override_get_db, override_get_current_user, client, app, test_user
from routers.auth import ALGORITHM, SECRET_KEY, create_access_token, get_db, authenticate_user, get_current_user
from jose import jwt
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db



def test_authenticate_user(test_user):
    db = TestingSessionLocal()


    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("testuser", "testpassword", db)
    assert non_existent_user is False

    wrong_password = authenticate_user(test_user.username, "testp@ssword", db)
    assert wrong_password is False


def test_create_access_token(test_user):
    username = "Jad"
    user_id = 1
    role = "admin"
    expires_delta = timedelta(days=1)
    
    token = create_access_token(username, user_id, role, expires_delta) 
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
          encode = {"sub": "Jad", "id": 1, "role": "admin"}
          token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

          current_user = await get_current_user(token)
          assert current_user == {"username": "Jad", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
          encode = {"role": "user"}
          token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

          with pytest.raises(HTTPException) as excinfo:
              await get_current_user(token=token)
          
          assert excinfo.value.status_code == 401
          assert excinfo.value.detail == "Could not validate user."


