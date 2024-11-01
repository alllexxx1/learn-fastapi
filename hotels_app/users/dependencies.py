from fastapi import Depends, Request

from jose import jwt, JWTError, ExpiredSignatureError

from config import settings
from hotels_app.users.dao import UserDAO
import exeptions


def get_token(request: Request) -> str:
    token = request.cookies.get('booking_access_token')

    if not token:
        raise exeptions.NoTokenException

    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.HASH_ALGORITHM
        )
    except ExpiredSignatureError:
        raise exeptions.ExpiredTokenException
    except JWTError:
        raise exeptions.IncorrectTokenFormatException

    user_id: str = payload.get('sub')
    if not user_id:
        raise exeptions.InsufficientPayloadDataException

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise exeptions.NoSuchUserException

    return user


# # Example of Admin role implementing
# # Here we check if the current user is Admin using a chain of dependencies
# async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
#     if current_user.role != 'admin':  # We have to have "role" field in "Users" table
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail='You have no rights'
#         )
#     admin_user = current_user
#     return admin_user
