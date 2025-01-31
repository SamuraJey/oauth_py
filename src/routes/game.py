# routes/game.py
from flask import Blueprint, current_app, render_template, session

from src.app.config.constants import DEFAULT_USER
from src.utils.decorator import login_required

bp = Blueprint("game", __name__)


@bp.route("/life")
@login_required
def life():
    user = session["user"] if "user" in session else DEFAULT_USER
    current_app.logger.info("Rendering life for user: %s", user)
    return render_template("life.html", user=user)
