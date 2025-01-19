from typing import cast

import pycouchdb
import requests
from flask import current_app

from dotenv_load import SiteSettings


def get_url(settings: SiteSettings) -> str:
    login = settings.couchdb_user
    password = settings.couchdb_password
    url = settings.couchdb_url
    port = settings.couchdb_port
    return f'http://{login}:{password}@{url}:{port}'

# curl -X PUT http://adm:pass@127.0.0.1:5984/_users

# curl -X PUT http://adm:pass@127.0.0.1:5984/_replicator


def create_system_dbs(settings: SiteSettings) -> None:
    base_url = get_url(settings)
    system_dbs = ['_users', '_replicator']

    for db in system_dbs:
        response = requests.put(f'{base_url}/{db}')
        if response.status_code in (201, 202):
            print(f"Created system database {db}")
        elif response.status_code == 412:
            print(f"System database {db} already exists")
        else:
            print(f"Failed to create system database {db}: {response.status_code}")


def get_db(settings: SiteSettings, database_name: str) -> pycouchdb.client.Database:
    full_url = get_url(settings)
    couchdb_server = pycouchdb.Server(full_url)
    create_system_dbs(settings)
    db = None
    try:
        db = couchdb_server.database(database_name)
    except pycouchdb.exceptions.NotFound:
        db = couchdb_server.create(database_name)
    return cast(pycouchdb.client.Database, db)
