import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from functools import wraps
from dotenv import load_dotenv
import pycouchdb

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

PORT = os.environ.get('PORT', 8080)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.debug = os.environ.get('DEBUG', False)
# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('App startup')

# OAuth configuration
oauth = OAuth(app)
oauth.register(
    name='vk',
    client_id=os.environ.get('VK_CLIENT_ID'),
    client_secret=os.environ.get('VK_CLIENT_SECRET'),
    authorize_url='https://oauth.vk.com/authorize',
    authorize_params=None,
    access_token_url='https://oauth.vk.com/access_token',
    access_token_params=None,
    refresh_token_url=None,
    # redirect_uri='http://localhost:8080/auth/',
    redirect_uri=os.environ.get('REDIRECT_URI'),
    client_kwargs={'scope': 'email'}
)


couchdb_server = pycouchdb.Server(os.environ.get('COUCHDB_URL'))
db = couchdb_server.database('notes')

DEFAULT_USER = 'Anonymous'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if app.debug is True:
                return f(*args, **kwargs)
            app.logger.info('User not in session, redirecting to login')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    user = session['user'] if 'user' in session else None
    app.logger.info('Rendering index for user: %s', user)
    return render_template('index.html', user=user)


@app.route('/login')
def login():
    app.logger.info('Rendering login page')
    return render_template('login.html')


@app.route('/authorize')
def authorize():
    redirect_uri = url_for('auth', _external=True, _scheme='https')
    app.logger.info('Redirecting to VK authorize URL: %s', redirect_uri)
    return oauth.vk.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.vk.authorize_access_token(
        client_id=oauth.vk.client_id,
        client_secret=oauth.vk.client_secret)
    user = oauth.vk.get('https://api.vk.com/method/users.get', params={'access_token': token['access_token'], 'v': '5.131'}).json()
    session['user'] = user['response'][0]
    app.logger.info('User authenticated: %s', user['response'][0])
    app.logger.info('session: %s', session)
    return redirect('/')


@app.route('/logout')
def logout():
    user = session.pop('user', None)
    app.logger.info('User logged out: %s', user)
    return redirect('/')


@app.route('/bingo', methods=['GET', 'POST'])
@login_required
def bingo():
    words = []
    user = session['user'] if 'user' in session else DEFAULT_USER
    if request.method == 'POST':
        words_str = request.form['words']
        words = [word.strip() for word in words_str.split(',') if word.strip()]
        if len(words) < 1:
            app.logger.warning('No words entered for bingo by user %s', session['user'])
            return render_template('index.html', error="Введите хотя бы одно слово", user=user)
        rows = int(len(words)**0.5) + 1
        cols = (len(words) + rows - 1) // rows
        words_grid = [words[i:i+cols] for i in range(0, len(words), cols)]
        app.logger.info('Bingo words grid created, rows: %s, cols: %s, by user %s', rows, cols, session['user'])
    else:
        words_grid = []

    return render_template('index.html', words_grid=words_grid, user=user)


@app.route('/mark_word', methods=['POST'])
@login_required
def mark_word():
    return jsonify({'success': True})


@app.route('/life')
@login_required
def life():
    user = session['user'] if 'user' in session else DEFAULT_USER
    app.logger.info('Rendering life for user: %s', user)
    return render_template('life.html', user=user)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes_view():
    user = session['user'] if 'user' in session else DEFAULT_USER
    if request.method == 'POST':
        note = request.form['note']
        db.save({'user': user, 'note': note})
        app.logger.info('Note added by user: %s', user)
        app.logger.debug('Note added: %s', note)
        return redirect(url_for('notes_view'))  # Redirect to avoid resubmission

    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page

    notes = db.query('notes/all_notes', skip=skip, limit=per_page, reduce=False)
    total_notes = db.query('notes/all_notes', reduce=True, as_list=True)[0]['value']
    notes_list = [{'user': note['value']['user'], 'note': note['value']['note']} for note in notes]

    total_pages = (total_notes + per_page - 1) // per_page

    return render_template('notes.html', notes=notes_list, user=user, page=page, total_pages=total_pages)


if __name__ == '__main__':
    debug_state = os.environ.get('DEBUG', 'False')
    if debug_state == 'False':
        app.debug = False
    elif debug_state == 'True':
        app.debug = True
    else:
        app.debug = False
    app.run(port=PORT, host='0.0.0.0')
