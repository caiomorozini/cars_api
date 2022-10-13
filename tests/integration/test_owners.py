from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_owners_sucess():
    with TestClient(app) as client:
        response = client.get('/api/v0/owners/')
    assert response.status_code == 200
    assert response.json() == []

# def test_get_owner_by_email_sucess():
#     with TestClient(app) as client:
#         response = client.get('/api/v0/owners/')
#     assert response.status_code == 200
#     assert response.json()['message'] == 'Owner created successfully'

# def test_create_new_user_sucess():
#     with TestClient(app) as client:
#         response = client.post('/api/v0/auth/create', json={
#           "name": "John Doe",
#           "email": "john@example.com"
#         }
      # )

# def test_create_new_owner_sucess():
#     with TestClient(app) as client:
#         response = client.post('/api/v0/owners/', json={
#           "name": "John Doe",
#           "email": "john@example.com",
#           "sale_opportunity": True
#         })
#     assert response.status_code == 200
#     assert response.json()['message'] == 'Owner created successfully'