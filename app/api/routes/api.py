from fastapi import APIRouter
from app.api.routes import (
    auth,
    cars,
    owners
)
from flask import Blueprint
from app.api.routes.flask_routes import (
  api as flask_blueprint
)
# Creating a blueprint
router = APIRouter(prefix="/api/v0")
blueprint = Blueprint('api_router', __name__, url_prefix="/api/v0")

# Adding routes to the blueprint
router.include_router(
  cars.router,
  tags=["Cars"],
  prefix="/cars"
)

router.include_router(
  owners.router,
  tags=["Owners"],
  prefix="/owners"
)

router.include_router(
  auth.router,
  tags=["Auth"],
  prefix="/auth"
)

blueprint.register_blueprint(
  flask_blueprint.blueprint)
