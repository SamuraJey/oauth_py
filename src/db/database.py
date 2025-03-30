import json
from typing import cast

import pycouchdb
import requests
from pycouchdb import exceptions

from app.config.dotenv_load import SiteSettings


def get_url(settings: SiteSettings) -> str:
    login = settings.couchdb_user.get_secret_value()
    password = settings.couchdb_password.get_secret_value()
    url = settings.couchdb_url
    port = settings.couchdb_port

    return f"http://{login}:{password}@{url}:{port}"


# curl -X PUT http://adm:pass@127.0.0.1:5984/_users

# curl -X PUT http://adm:pass@127.0.0.1:5984/_replicator


def add_design_document(settings: SiteSettings, db_name: str) -> None:
    base_url = get_url(settings)
    # db_name = 'notes'
    design_doc = {
        "_id": "_design/notes",
        "views": {
            "all_notes": {
                "map": "function(doc) { if (doc.user && doc.note) { emit(doc._id, {'user':doc.user, 'note':doc.note}); } }",  # noqa
                "reduce": "_count",
            }
        },
    }

    url = f"{base_url}/{db_name}/_design/notes"
    headers = {"Content-Type": "application/json"}

    response = requests.put(url, headers=headers, data=json.dumps(design_doc))

    if response.status_code in (201, 202):
        print("Design document added successfully.")
    elif response.status_code == 409 or response.status_code == 412:
        print("Design document already exists.")
    else:
        print(f"Failed to add design document: {response.status_code} - {response.text}")


def create_system_dbs(settings: SiteSettings) -> None:
    base_url = get_url(settings)
    system_dbs = ["_users", "_replicator"]

    for db in system_dbs:
        response = requests.put(f"{base_url}/{db}")
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
    add_design_document(settings, database_name)
    db = None
    try:
        db = couchdb_server.database(database_name)
    except exceptions.NotFound:
        db = couchdb_server.create(database_name)
    return cast(pycouchdb.client.Database, db)
