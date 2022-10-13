# cars_api

This is a simple API for cars. It is a REST API that allows you to create, read, update and delete cars.
In order to create a car, you need to create a owner first.

## Installation
To install dependencies, run:
```bash
poetry install
```
Create a .env file and add the values on env_example.

Run docker-compose:
```bash
docker-compose up
```
Finally run the application:
```bash
poetry run uvicorn app.main:app --reload
```

## Usage
To use the API, you need to create a user first. To do that, you need to send a POST request to the endpoint /api/v0/auth/create with the following body:
```json
{
    "email": "caio@example.com",
    "password": "123456"
}
```
The response will be:
```json
{
    "id": UUID,
    "email": "caio@example.com",
    "created_at": now()
}
```
To get the token, you need to send a POST request to the endpoint /api/v0/auth/token with the following body:
```json
{
    "username": "caio@example.com",
    "password": "123456"
}
```
The response will be:
```json
{
    "access_token": "TOKEN",
    "token_type": "bearer"
}
```
Now you can use the token to access the other endpoints. To do that, you need to add the token to the header of the request:
```json
{
    "Authorization": "Bearer TOKEN"
}
```
To create a car, first you need to create a owner. To do that, you need to send a POST request to the endpoint /api/v0/owners with the following body:
```json
{
    "name": "Caio",
    "email": "caio@example.com",
}
```
The response will be:
```json
{
    "message": "Owner created successfully"
}
```
To create a car, you need to send a POST request to the endpoint /api/v0/cars with the following body:
```json
{
    "owner_email": "caio@example.com",
    "model": "sedan",
    "color": "yellow"
}
```

The response will be:
```json
{
    "message": "Car created successfully"
}
```
To get all cars, you need to send a GET request to the endpoint /api/v0/cars. The response will be:
```json
[
    {
        "id": UUID,
        "owner_email": "caio@example.com",
        "model": "sedan",
        "color": "yellow",
        "created_at": now()
    }
]
```
To get a car, you need to send a GET request to the endpoint /api/v0/cars/{owner_email}. The response will be:
```json
{
    "id": UUID,
    "owner_email": "caio@example.com",
    "model": "sedan",
    "color": "yellow",
    "created_at": now()
}
```
To update a car, you need to send a PUT request to the endpoint /api/v0/cars/{owner_email} with the following body:
```json
{
    "model": "sedan",
    "color": "yellow"
}
```
The response will be:
```json
{
    "message": "Car updated successfully"
}
```
To delete a car, you need to send a DELETE request to the endpoint /api/v0/cars/{owner_email}. The response will be:
```json
{
    "message": "Car deleted successfully"
}
```

## Tests
To run the tests, run:
```bash
poetry run pytest
```

## Swagger
To access the swagger, go to http://localhost:8000/docs# and use the token to access the endpoints. Also, you can access the swagger on http://localhost:8000/redoc.

## Acess Flask endpoints
To acess the flask endpoint, go to http://localhost:8000/flask.
There you can navigate through the endpoints: /flask/owners and /flask/cars to read the owners and cars.

## Structure
The structure of the project is:
```
.
├── app
│   ├── api
│   │   ├── routes
│   │   │   ├── api.py
│   │   │   ├── cars.py
│   │   │   ├── owners.py
│   │   │   └── auth.py
│   │   │   └── flask_routes
│   │   │       ├── api.py
│   │   │       ├── cars.py
│   │   │       └── owners.py
│   │── core
│   │   ├── config.py
│   │── db
│   │   ├── database.py
│   │── resources
│   │   ├── oauth2.py
│   │   ├── utils.py
│   │── schemas
│   │   ├── auth.py
│   │   ├── schemas.py
│   │── static
│   │   ├── app.css
│   │   ├── bootstrap.css
│   ├── templates
│   │   ├── car.html
│   │   ├── owner.html
│   │   ├── template.html
│   ├── main.py
├── tests
│   ├── integration
│   │   ├── database.py
│   │   ├── tests.py
