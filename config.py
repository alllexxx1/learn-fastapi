from typing import Literal

from pydantic import ConfigDict, SecretStr, root_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']
    SECRET_KEY: str
    HASH_ALGORITHM: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_TEST_HOST: str
    DB_TEST_PORT: int
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return (
            f'postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@'
            f'{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}'
        )

    REDIS_HOST: str
    REDIS_PORT: int
    # REDIS_USER: str
    # REDIS_USER_PASSWORD: str

    @property
    def REDIS_URL(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    # @property
    # def REDIS_URL(self):
    #     return f'redis://{self.REDIS_USER}:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0'

    IMAP_SMTP_HOST: str
    IMAP_SMTP_PORT: int
    IMAP_SMTP_USERNAME: str
    IMAP_SMTP_PASSWORD: str

    # @root_validator(skip_on_failure=True)
    # def get_database_url(cls, v):
    #     v['DATABASE_URL'] = f'postgresql+asyncpg://{v["DB_USER"]}:{v["DB_PASS"]}@{v["DB_HOST"]}:{v["DB_PORT"]}/{v["DB_NAME"]}'
    #     return v

    # @property
    # def DATABASE_URL(self):
    #     return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = ConfigDict(env_file='.env')

    # Deprecated structure
    # class Config:
    #     env_file = '.env'


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
