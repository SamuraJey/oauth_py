from typing import cast
import pycouchdb

from dotenv_load import SiteSettings

def get_url(settings: SiteSettings) -> str:
    login = settings.couchdb_user
    password = settings.couchdb_password
    url = settings.couchdb_url
    port = settings.couchdb_port
    return f'http://{login}:{password}@{url}:{port}'

def get_db(settings: SiteSettings, database_name: str) -> pycouchdb.client.Database:
    full_url = get_url(settings)
    couchdb_server = pycouchdb.Server(full_url)
    try:
        db = couchdb_server.database(database_name)
    except pycouchdb.exceptions.NotFound:
        db = couchdb_server.create(database_name)
    return cast(pycouchdb.client.Database, db)
