import requests
from flask import Blueprint, render_template

blueprint = Blueprint('cars', __name__)

@blueprint.route('/', methods=['GET'])
async def get_owners(
  skip: int = 0,
  take: int = 20
):
    url = f'http://localhost:8000/api/v0/cars/?skip={skip}&take={take}'
    return render_template(
        'car.html',
        cars=requests.get(
            url,timeout=30).json())
