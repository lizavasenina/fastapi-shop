"""Module providing a configuration of database."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Class contains database settings"""
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            ".env"))
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def db_url(self):
        """Property returns database URL"""
        return (
            "postgresql+psycopg://" +
            f"{self.POSTGRES_USER}:" +
            f"{self.POSTGRES_PASSWORD}@" +
            f"{self.POSTGRES_HOST}:" +
            f"{self.POSTGRES_PORT}/" +
            f"{self.POSTGRES_DB}"
        )
    
settings = Settings()
