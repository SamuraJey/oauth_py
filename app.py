from authlib.integrations.flask_client import OAuth
from flask import Flask
from pycouchdb.client import Database

from database import get_db
from dotenv_load import SiteSettings
from logger import setup_logger
from oauth import get_oauth
from routes import index


class MyFlask(Flask):
    oauth: OAuth
    db: Database


def create_app(settings: SiteSettings) -> MyFlask:
    app = MyFlask(__name__)
    app.secret_key = settings.flask_secret_key
    app.debug = settings.debug

    # Configure logging
    logger = setup_logger(app)
    logger.info('App startup')

    # OAuth configuration
    app.oauth = get_oauth(app, settings)
    app.db = get_db(settings)

    # Register blueprints
    from routes import auth, game, notes
    app.register_blueprint(auth.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(index.bp)

    return app


if __name__ == '__main__':
    settings = SiteSettings()
    app = create_app(settings)

    if app.debug:
        app.run(port=settings.port, host='0.0.0.0')
    else:
        from waitress import serve
        serve(app, port=settings.port, host='0.0.0.0', _quiet=False)
