from flask import Blueprint, current_app, render_template, session

from app.config.constants import DEFAULT_USER
from utils.decorator import login_required

bp = Blueprint("index", __name__)


@bp.route("/")
@login_required
def index():
    user = session.get("user", DEFAULT_USER)
    current_app.logger.info("Rendering index for user: %s", user)
    return render_template("index.html", user=user)
