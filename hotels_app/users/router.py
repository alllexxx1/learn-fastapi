from alembic.command import current
from fastapi import APIRouter, Depends, Response

from hotels_app.users.dependencies import get_current_user
from hotels_app.users.models import Users
from hotels_app.users.schemas import SchemaUserAuth, SchemaUser
from hotels_app.users.dao import UserDAO
from hotels_app.users.auth import get_password_hash, verify_password, create_access_token
from exeptions import UserAlreadyExistsException, IncorrectCredentialsException, NoRightsException


router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)


@router.post('/register')
async def register_user(user_data: SchemaUserAuth) -> None:
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add_one(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login(response: Response, user_data: SchemaUserAuth) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise IncorrectCredentialsException

    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout(response: Response) -> None:
    response.delete_cookie('booking_access_token')


@router.get('/me')
async def read_current_user_info(
        current_user: Users = Depends(get_current_user)
) -> SchemaUser:
    return current_user


# # Example of router access to which is given only to Admin user
# @router.get('/all')
# async def read_all_users_info(current_admin_user: Users = Depends(get_current_admin_user)):
#     all_users = await UserDAO.find_all()
#     return all_users
