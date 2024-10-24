from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from models import db
from auth import bp as auth_bp, init_login_manager
from book import bp as book_bp
from review import bp as review_bp
# from courses import bp as courses_bp

app = Flask(__name__)
application = app

app.config.from_pyfile("config.py")

db.init_app(app)
migrate = Migrate(app, db)

init_login_manager(app)


@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(err):
    error_msg = (
        "Возникла ошибка при подключении к базе данных. " "Повторите попытку позже."
    )
    return f"{error_msg} (Подробнее: {err})", 500


app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)


@app.route("/")
def index():
    return redirect(url_for("book.index"))
