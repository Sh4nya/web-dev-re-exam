from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from models import db, User
from functools import wraps

bp = Blueprint("auth", __name__, url_prefix="/auth")


def check_rights(rule):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # user = load_user(kwargs.get("user_id", None))
            if not current_user.is_authenticated:
                flash(
                    "Для выполнения данного действия необходимо пройти процедуру аутентификации",
                    "warning",
                )
                return redirect(url_for("auth.login"))
            if current_user.can(rule):
                return f(*args, **kwargs)
            flash("У вас недостаточно прав для выполнения данного действия", "warning")
            return redirect(url_for("index"))

        return decorated_function

    return decorator


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Для выполнения данного действия необходимо пройти процедуру аутентификации"
    )
    login_manager.login_message_category = "warning"
    login_manager.user_loader(load_user)
    login_manager.init_app(app)


def load_user(user_id):
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    return user


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if login and password:
            user = db.session.execute(db.select(User).filter_by(login=login)).scalar()
            print(login, password)
            if user and user.check_password(password):
                login_user(user)
                flash("Вы успешно аутентифицированы.", "success")
                next = request.args.get("next")
                return redirect(next or url_for("index"))
        flash("Введены неверные логин и/или пароль.", "danger")
    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))
