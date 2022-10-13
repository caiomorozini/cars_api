from flask import Blueprint
from app.api.routes.flask_routes import (
  owners, cars
)

blueprint = Blueprint('api', __name__)

blueprint.register_blueprint(
  owners.blueprint, url_prefix='/owners')
blueprint.register_blueprint(
  cars.blueprint, url_prefix='/cars')
