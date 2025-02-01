from authlib.integrations.flask_client import OAuth
from flask import Flask
from pycouchdb.client import Database

from app.config.dotenv_load import SiteSettings
from db.database import get_db
from oauth.oauth import get_oauth
from utils.logger import setup_logger


class MyFlask(Flask):
    oauth: OAuth
    db: Database


def create_app(settings: SiteSettings) -> MyFlask:
    app = MyFlask(__name__)
    app.secret_key = settings.flask_secret_key.get_secret_value()
    app.debug = settings.debug

    logger = setup_logger(app)
    logger.info("App startup")

    app.oauth = get_oauth(app, settings)
    app.db = get_db(settings, "notes")

    from routes import auth, game, index, notes

    app.register_blueprint(auth.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(index.bp)

    return app


if __name__ == "__main__":
    settings = SiteSettings()
    print(settings.model_dump())
    app = create_app(settings)

    if app.debug:
        app.run(port=settings.port, host="0.0.0.0")
    else:
        from waitress import serve

        serve(app, port=settings.port, host="0.0.0.0", _quiet=False)
