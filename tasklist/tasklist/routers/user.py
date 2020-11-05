# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
from typing import Dict

from fastapi import APIRouter, HTTPException, Depends

from ..database import DBSession, get_db
from ..models import User

router = APIRouter()


@router.get(
    '',
    summary='Reads user list',
    description='Reads the whole user list.',
    response_model=Dict[str, User],
)
async def read_users(db: DBSession = Depends(get_db)):
    return db.read_users()


@router.post(
    '',
    summary='Creates a new user',
    description='Creates a new user.',
    response_model=str,
)
async def create_user(item: User, db: DBSession = Depends(get_db)):
    return db.create_user(item)


@router.get(
    '/{username_}',
    summary='Reads user',
    description='Reads user from username.',
    response_model=User,
)
async def read_user(username_: str, db: DBSession = Depends(get_db)):
    try:
        return db.read_user(username_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception


@router.put(
    '/{username_}',
    summary='Replaces a user',
    description='Replaces a user identified by its username.',
)
async def replace_username(
        username_: str,
        item: User,
        db: DBSession = Depends(get_db),
):
    try:
        db.replace_user(username_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception


@router.patch(
    '/{username_}',
    summary='Alters user',
    description='Alters a user identified by its username',
)
async def alter_user(
        username_: str,
        item: User,
        db: DBSession = Depends(get_db),
):
    try:
        old_item = db.read_user(username_)
        update_data = item.dict(exclude_unset=True)
        new_item = old_item.copy(update=update_data)
        db.replace_user(username_, new_item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception


@router.delete(
    '/{username_}',
    summary='Deletes user',
    description='Deletes a user identified by its username',
)
async def remove_user(username_: str, db: DBSession = Depends(get_db)):
    try:
        db.remove_user(username_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception


@router.delete(
    '',
    summary='Deletes all users, use with caution',
    description='Deletes all users, use with caution',
)
async def remove_all_users(db: DBSession = Depends(get_db)):
    db.remove_all_users()
