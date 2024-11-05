from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

PORT=os.environ.get('PORT', 8080)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

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
    redirect_uri='http://localhost/auth',
    client_kwargs={'scope': 'email'}
)


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    return render_template('index.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.vk.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():

    token = oauth.vk.authorize_access_token(
        client_id=oauth.vk.client_id,
        client_secret=oauth.vk.client_secret)
    user = oauth.vk.get('https://api.vk.com/method/users.get', params={'access_token': token['access_token'], 'v': '5.131'}).json()
    session['user'] = user['response'][0]
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/bingo', methods=['GET', 'POST'])
def bingo():
    if 'user' not in session:
        return redirect(url_for('login'))
    words = []
    if request.method == 'POST':
        words_str = request.form['words']
        words = [word.strip() for word in words_str.split(',') if word.strip()]
        if len(words) < 1:
            return render_template('index.html', error="Введите хотя бы одно слово")
        rows = int(len(words)**0.5) + 1
        cols = (len(words) + rows - 1) // rows
        words_grid = [words[i:i+cols] for i in range(0, len(words), cols)]
    else:
        words_grid = []

    return render_template('index.html', words_grid=words_grid, user=session['user'])


@app.route('/mark_word', methods=['POST'])
def mark_word():
    if 'user' not in session:
        return redirect(url_for('login'))
    word = request.form['word']
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=PORT, host='0.0.0.0')
