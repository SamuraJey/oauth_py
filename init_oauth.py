from authlib.integrations.flask_client import OAuth


def init_oauth(app, settings):
    oauth = OAuth(app)
    oauth.register(
        name='vk',
        client_id=settings.vk_client_id,
        client_secret=settings.vk_client_secret,
        access_token_url='https://oauth.vk.com/access_token',
        access_token_params=None,
        authorize_url='https://oauth.vk.com/authorize',
        authorize_params=None,
        api_base_url='https://api.vk.com/',
        client_kwargs={'scope': 'email'},
    )
    return oauth