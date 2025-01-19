from typing import cast
import pycouchdb

from dotenv_load import SiteSettings


def get_db(settings: SiteSettings) -> pycouchdb.client.Database:
    couchdb_server = pycouchdb.Server(settings.couchdb_url)
    db = couchdb_server.database('notes')
    return cast(pycouchdb.client.Database, db)
