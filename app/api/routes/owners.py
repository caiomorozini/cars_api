import logging
from fastapi import (
    APIRouter,
    HTTPException,
    Response,
    status,
    Depends
)
from app.db.database import (
    database, owners
)
from app.schemas import schema
from app.resources import oauth2


router = APIRouter()


@router.get('/')
async def get_owners(
    skip: int=0,
    take: int = 20,
    # user_id: int = Depends(oauth2.get_current_user)
    ):
    """Get all owners"""
    query = owners.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_owner(
    owner: schema.NewOwner,
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """Create a new owner"""
    query = owners.insert().values(
        **owner.dict()
    )
    await database.execute(query)
    return {'message': 'Owner created successfully'}

@router.get('/{email}', status_code=status.HTTP_200_OK)
async def get_owner(
    email: str,
    # user_id: int = Depends(oauth2.get_current_user)
    ):
    """Get a owner by email"""
    query = owners.select().where(owners.c.email == email)
    return await database.fetch_one(query)

@router.put('/{email}', status_code=status.HTTP_204_NO_CONTENT)
async def update_owner(
    email: str,
    updated_owner: schema.NewOwner,
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """Update a owner by email

    Args:
        email (str): Email of the owner
        updated_owner (schema.NewOwner): New owner data

    Returns:
        [bool]: True if the owner was updated
    """
    # Selecting the owner
    selected_owner = owners.select().where(owners.c.email == email)

    sid = await database.fetch_one(selected_owner)
    if not sid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Owner with email: {email} does not exist'
        )
    else:
        query = owners.update().where(owners.c.email == email).values(
            **updated_owner.dict()
            )
        await database.execute(query)
        logging.info('Owner changed successfully')
        return {'message': 'Owner changed successfully'}

@router.delete('/{email}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_owner(
    email: str,
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """Remove a owner by email

    Args:
        email (str): Email of the owner

    Returns:
        [bool]: True if the owner was removed
    """
    # Selecting the owner
    selected_owner = owners.select().where(owners.c.email == email)

    sid = await database.fetch_one(selected_owner)
    if not sid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Owner with email: {email} does not exist'
        )
    else:
        query = owners.delete().where(owners.c.email == email)
        await database.execute(query)
        logging.info('Owner removed successfully')
        return {'message': 'Owner removed successfully'}
