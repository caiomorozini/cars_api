from typing import Optional
from pydantic import BaseModel, constr
from pydantic.networks import EmailStr


class NewOwner(BaseModel):
    """Template for owner creation"""
    name: constr(
        min_length=3,
        max_length=50,
        strip_whitespace=True,
        regex=r'^[a-zA-Z ]+$',
        ) = "Name Example"
    email: EmailStr
    sale_opportunity: Optional[bool] = True

class NewCar(BaseModel):
    """Template for car creation"""
    model: constr(
        min_length=3,
        max_length=11,
        regex='hatch|sedan|convertible',
        strip_whitespace=True,
        to_lower=True,
    )

    color: constr(
        min_length=3,
        max_length=11,
        regex='(yellow|blue|gray)',
        strip_whitespace=True,
        to_lower=True,
    )
    owner_email: EmailStr

class UpdateCar(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    color: constr(
        min_length=3,
        max_length=11,
        regex='(yellow|blue|gray)',
        strip_whitespace=True,
        to_lower=True,
    )
