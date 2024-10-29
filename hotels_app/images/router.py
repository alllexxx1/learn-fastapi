from fastapi import UploadFile, APIRouter
import shutil

from hotels_app.tasks.tasks import process_picture

router = APIRouter(
    prefix='/images',
    tags=['Images upload']
)


@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile):
    image_path = f'hotels_app/static/images/{name}.webp'
    with open(image_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_picture.delay(image_path)
