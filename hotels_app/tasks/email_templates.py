from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,
) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Booking confirmation'
    email['From'] = settings.IMAP_SMTP_USERNAME
    email['To'] = email_to

    email.set_content(
        f'''
        <h1>Confirm booking, please</h1>
        You've booked a room from {booking['date_from']}
        to {booking['date_to']}
        ''',
        subtype='html'
    )

    return email
