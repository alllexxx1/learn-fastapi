from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import root_validator, SecretStr


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    HASH_ALGORITHM: str

    # @root_validator(skip_on_failure=True)
    # def get_database_url(cls, v):
    #     v['DATABASE_URL'] = f'postgresql+asyncpg://{v["DB_USER"]}:{v["DB_PASS"]}@{v["DB_HOST"]}:{v["DB_PORT"]}/{v["DB_NAME"]}'
    #     return v

    class Config:
        env_file = '.env'


# class Settings(BaseSettings):
#     DB_HOST: SecretStr
#     DB_PORT: int
#     DB_USER: SecretStr
#     DB_PASS: SecretStr
#     DB_NAME: SecretStr
#
#     model_config = SettingsConfigDict(
#         env_file='.env',
#         env_file_encoding='utf-8'
#     )


settings = Settings()
