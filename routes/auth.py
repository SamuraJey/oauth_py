from flask import (Blueprint, current_app, redirect, render_template, session,
                   url_for)

bp = Blueprint('auth', __name__)


@bp.route('/login')
def login():
    current_app.logger.info('Rendering login page')
    return render_template('login.html')


@bp.route('/authorize')
def authorize():
    redirect_uri = url_for('auth.auth', _external=True, _scheme='https')
    current_app.logger.info('Redirecting to VK authorize URL: %s', redirect_uri)
    return current_app.oauth.vk.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    token = current_app.oauth.vk.authorize_access_token(
        client_id=current_app.oauth.vk.client_id,
        client_secret=current_app.oauth.vk.client_secret)
    user = current_app.oauth.vk.get('https://api.vk.com/method/users.get',
                                    params={'access_token': token['access_token'], 'v': '5.131'}).json()
    session['user'] = user['response'][0]
    current_app.logger.info('User authenticated: %s', user['response'][0])
    return redirect(url_for('index.index'))


@bp.route('/logout')
def logout():
    user = session.pop('user', None)
    current_app.logger.info('User logged out: %s', user)
    return redirect(url_for('index.index'))
