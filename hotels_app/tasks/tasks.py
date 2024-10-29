from pathlib import Path
import smtplib

from pydantic import EmailStr

from PIL import Image

from config import settings
from hotels_app.tasks.celery_app import celery_app
from hotels_app.tasks.email_templates import (
    create_booking_confirmation_template
)


@celery_app.task
def process_picture(
    path: str
):
    image_path = Path(path)
    image = Image.open(image_path)

    resized_image = image.resize((1000, 800))
    resized_image.save(f'hotels_app/static/images/standardized_{image_path.name}')


@celery_app.task
def send_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.IMAP_SMTP_HOST, settings.IMAP_SMTP_PORT) as server:
        server.login(settings.IMAP_SMTP_USERNAME, settings.IMAP_SMTP_PASSWORD)
        server.send_message(email_content)
