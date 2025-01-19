from typing import cast
from flask import current_app
import pycouchdb

from dotenv_load import SiteSettings


def get_url(settings: SiteSettings) -> str:
    login = settings.couchdb_user
    password = settings.couchdb_password
    url = settings.couchdb_url
    port = settings.couchdb_port
    return f'http://{login}:{password}@{url}:{port}'

# curl -X PUT http://adm:pass@127.0.0.1:5984/_users

# curl -X PUT http://adm:pass@127.0.0.1:5984/_replicator


def init_db(couch_db_server: pycouchdb.Server) -> None:

    try:
        couch_db_server.create('_users')
    except pycouchdb.exceptions.Conflict:
        current_app.logger.info('Database _users already exists')
        pass

    try:
        couch_db_server.create('_replicator')
    except pycouchdb.exceptions.Conflict:
        current_app.logger.info('Database _replicator already exists')
        pass


def get_db(settings: SiteSettings, database_name: str) -> pycouchdb.client.Database:
    full_url = get_url(settings)
    couchdb_server = pycouchdb.Server(full_url)
    init_db(couchdb_server)
    db = None
    try:
        db = couchdb_server.database(database_name)
    except pycouchdb.exceptions.NotFound:
        db = couchdb_server.create(database_name)
    return cast(pycouchdb.client.Database, db)
