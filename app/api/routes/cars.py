from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
)
from app.resources import oauth2
from app.db.database import (
    database, cars, owners
)
from app.schemas import schema

router = APIRouter()

@router.get('/')
async def get_all_cars(
    skip: int=0,
    take: int = 20,
    # user_id: int = Depends(oauth2.get_current_user)
    ):
    """_summary_

    Args:
        skip (int, optional): _description_. Defaults to 0.
        take (int, optional): _description_. Defaults to 20.

    Returns:
        _type_: _description_
    """
    query = cars.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@router.get('/{car_id}', status_code=status.HTTP_200_OK)
async def get_car(
    car_id: str,
    # user_id: int = Depends(oauth2.get_current_user)
    ):
    """Get a car by id

    Args:
        car_id (int): _description_

    Returns:
        _type_: _description_
    """
    query = cars.select().where(cars.c.id == car_id)
    return {
        'response': await database.fetch_one(query),
        'message': 'Car founded successfully'
    }

@router.get('/{owner_email}', status_code=status.HTTP_200_OK)
async def get_cars_by_owner(
    owner_email: str,
    # user_id: int = Depends(oauth2.get_current_user),
    ):
    """Get cars by owner email

    Args:
        owner_email (str): Email of the owner

    Returns:
        list[dict]: List of cars owned by the owner passed as argument
    """
    query = cars.select().where(cars.c.owner_email == owner_email)
    return {
        'response': await database.fetch_all(query),
        'message': 'Cars founded successfully',
    }

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_car(
    new_car: schema.NewCar,
    user_id: int = Depends(oauth2.get_current_user)
    ):

    sid = await database.execute(
        owners.select().where(owners.c.email == new_car.owner_email))
    if not sid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Owner with email: {new_car.owner_email} does not exist'
        )

    cars_ids: list = (
        await database.fetch_all(
            cars.select().where(cars.c.owner_email == new_car.owner_email))
    )

    if cars_ids:
        number_of_cars = len(cars_ids)
        if number_of_cars > 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Owner with email: {new_car.owner_email} already has 3 cars'
            )

    create_car = await database.execute(
        cars.insert().values(
            **new_car.dict()
    ))
    if not create_car:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not create car'
        )
    await database.execute(
        owners.update().where(owners.c.id == sid).values(
            sale_opportunity=False
    ))
    return {
        'message': 'Car created successfully',
        'status': 'success'
        }

@router.put('/{car_id}', status_code=status.HTTP_200_OK)
async def update_car(
    car_id: str,
    updated_car: schema.UpdateCar,
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """Update a car by id"""

    if not await database.fetch_one(cars.select().where(cars.c.id == car_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Owner with id: {car_id} does not exist'
        )

    query = cars.update().where(cars.c.id == car_id).values(**updated_car.dict())
    await database.execute(query)
    return {
        'message': 'Car updated successfully',
        'status': 'success'
    }

@router.delete('/{car_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: str,
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """Delete a car by id"""
    car_info = await database.fetch_one(cars.select().where(cars.c.id == car_id))
    if not car_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Owner with id: {car_id} does not exist'
        )

    await database.execute(cars.delete().where(cars.c.id == car_id))

    owner_email = car_info.get('owner_email', None)
    cars_share_owner = await database.fetch_all(
        cars.select().where(cars.c.owner_email == owner_email)
    )
    if len(cars_share_owner) <= 0:
        await database.execute(
            owners.update().where(owners.c.email == owner_email).values(
                sale_opportunity=True
    ))
    return {'message': 'Car deleted successfully'}
