from flask import (Blueprint, current_app, redirect, render_template, session,
                   url_for)

from constants import DEFAULT_USER
from decorator import login_required

bp = Blueprint('index', __name__)


@bp.route('/')
@login_required
def index():
    user = session['user'] if 'user' in session else DEFAULT_USER
    current_app.logger.info('Rendering index for user: %s', user)
    return render_template('index.html', user=user)
