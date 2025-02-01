from functools import wraps

from flask import current_app, redirect, session, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            if current_app.debug is True:
                return f(*args, **kwargs)
            current_app.logger.info("User not in session, redirecting to login")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function
