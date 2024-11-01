from datetime import datetime, date, timezone, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict

from fastapi import Query


class SchemaRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: list[str]
    quantity: int
    image_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

    # deprecated structure
    # class Config:
    #     from_attribute = True


class SchemaRoomInfo(SchemaRoom):
    rooms_left: int

    model_config = ConfigDict(
        from_attributes=True
    )

    # deprecated structure
    # class Config:
    #     from_attribute = True


class RoomSearchArgs:
    def __init__(
            self,
            date_from: date = Query(...,
                                    description=f'e.g. {datetime.now(timezone.utc).date()}'),
            date_to: date = Query(...,
                                  description=f'e.g. {(datetime.now(timezone.utc) + timedelta(days=14)).date()}')
    ):
        self.date_from = date_from
        self.date_to = date_to
