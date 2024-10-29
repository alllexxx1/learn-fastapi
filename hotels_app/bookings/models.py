from sqlalchemy import (
    Column, Computed, Date,
    Integer, ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey('rooms.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Computed('(date_to - date_from) * price'), nullable=False)
    total_days = Column(Computed('date_to - date_from'), nullable=False)

    user = relationship('Users', back_populates='booking')
    room = relationship('Rooms', back_populates='booking')

    def __str__(self):
        return f'Booking #{self.id}'
