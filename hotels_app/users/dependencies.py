from datetime import datetime, timezone
from fastapi import Depends, Request, HTTPException, status

from jose import jwt, JWTError

from config import settings
from hotels_app.users.dao import UserDAO

def get_token(request: Request) -> str:
    token = request.cookies.get('booking_access_token')

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='There is no token'
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.HASH_ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is not JWT'
        )

    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired'
        )

    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User_id is missed in token payload'
        )

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='There is no such user in DB'
        )

    return user


# # Example of Admin role implementing
# # Here we check if the current user is Admin using a chain of dependencies
# async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
#     if current_user.role != 'admin':  # We have to have "role" field in "Users" table
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='You have no rights'
#         )
#     admin_user = current_user
#     return admin_user
