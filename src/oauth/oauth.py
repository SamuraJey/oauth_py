from authlib.integrations.flask_client import OAuth
from flask import Flask

from dotenv_load import SiteSettings


def get_oauth(app: Flask, settings: SiteSettings) -> OAuth:
    oauth = OAuth(app)
    oauth.register(
        name='vk',
        client_id=settings.vk_client_id,
        client_secret=settings.vk_client_secret,
        authorize_url='https://oauth.vk.com/authorize',
        authorize_params=None,
        access_token_url='https://oauth.vk.com/access_token',
        access_token_params=None,
        refresh_token_url=None,  # Refresh token is not implemented
        # redirect_uri='http://localhost:8080/auth/',
        redirect_uri=settings.redirect_uri,
        client_kwargs={'scope': 'email'}
    )
    return oauth
