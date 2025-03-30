from dotenv import find_dotenv, load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

dotenv_name = os.getenv("DOTENV_NAME", ".env")
print(f"Loading dotenv file: {dotenv_name}")

DOTENV = find_dotenv(filename=dotenv_name, usecwd=True, raise_error_if_not_found=True)
load_dotenv(DOTENV, override=True)


class SiteSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    flask_secret_key: SecretStr
    vk_client_id: SecretStr
    vk_client_secret: SecretStr
    port: int = 8080
    debug: bool = False
    redirect_uri: SecretStr
    couchdb_url: str = "localhost"
    couchdb_port: int = 5984
    couchdb_user: SecretStr
    couchdb_password: SecretStr
