
# import pytest
# from jose import jwt
# from app.core.config import settings


# def test_create_user(client):
#     res = client.post(
#         "/api/v0/auth/create", json={"email": "caio@example.com", "password": "123456"})

#     assert res.json()['email'] == "caio@example.com"
#     assert res.status_code == 201

# def test_login_user(test_user, client):
#     res = client.post(
#         "/login", data={"username": test_user['email'], "password": test_user['password']})
#     login_res = res.json()
#     payload = jwt.decode(login_res.access_token,
#                          settings.secret_key, algorithms=[settings.algorithm])
#     id = payload.get("user_id")
#     assert id == test_user['id']
#     assert login_res['token_type'] == "bearer"
#     assert res.status_code == 200

