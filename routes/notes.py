# routes/notes.py
from flask import (Blueprint, current_app, redirect, render_template, request,
                   session, url_for)

from constants import DEFAULT_USER
from decorator import login_required

bp = Blueprint('notes', __name__)


@bp.route('/notes', methods=['GET', 'POST'])
@login_required
def notes_view():
    user = session['user'] if 'user' in session else DEFAULT_USER
    if request.method == 'POST':
        note = request.form['note']
        current_app.db.save({'user': f"{user.get('first_name', '')} {user.get('last_name', '')}", 'note': note})
        current_app.logger.info('Note added by user: %s', user)
        current_app.logger.debug('Note added: %s', note)
        return redirect(url_for('notes.notes_view'))

    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page

    notes = current_app.db.query('notes/all_notes', skip=skip, limit=per_page, reduce=False)

    total_notes = current_app.db.query('notes/all_notes', reduce=True, as_list=True)
    if len(total_notes) > 0:
        total_notes = total_notes[0]['value']
    else:
        total_notes = 0

    notes_list = [{'user': note['value']['user'], 'note': note['value']['note']} for note in notes]

    total_pages = (total_notes + per_page - 1) // per_page

    return render_template('notes.html', notes=notes_list, user=user, page=page, total_pages=total_pages)
