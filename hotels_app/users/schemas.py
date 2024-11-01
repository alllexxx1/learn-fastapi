from pydantic import BaseModel, ConfigDict, EmailStr


class SchemaUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        from_attributes=True
    )

    # deprecated structure
    # class Config:
    #     from_attributes = True
