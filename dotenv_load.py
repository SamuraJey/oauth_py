from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class SiteSettings(Settings):
    flask_secret_key: str
    vk_client_id: str
    vk_client_secret: str
    port: int = 8080
    debug: bool = False
    redirect_uri: str
    couchdb_url: str = 'localhost'
    couchdb_port: int = 5984
    couchdb_user: str
    couchdb_password: str
