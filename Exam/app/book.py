import os
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_from_directory,
)
from flask_login import login_required, current_user
from models import db, Genre, Book, GenreToBook, Review, Cover, User
from auth import check_rights
from nh3 import clean
from tools import CoverSaver, CoverRemover
from sqlalchemy.sql import func, and_
from markdown2 import markdown

bp = Blueprint("book", __name__, url_prefix="/book")

BOOK_PARAMS = ["title", "year", "publisher", "author", "length"]


def params():
    return {p: request.form.get(p) or None for p in BOOK_PARAMS}


@bp.route("/")
def index():
    books_query = (
        db.session.query(
            Book.id.label("id"),
            Book.title.label("title"),
            Book.description.label("description"),
            func.group_concat(Genre.name.distinct()).label("genres"),
            Book.year.label("year"),
            func.group_concat(Review.rating).label("review_rating"),
            func.group_concat(Review.status_id).label("review_status_ids"),
            Cover.filename.label("cover_filename"),
        )
        .outerjoin(GenreToBook, Book.id == GenreToBook.book_id)
        .outerjoin(Genre, Genre.id == GenreToBook.genre_id)
        .outerjoin(Review, Book.id == Review.book_id)
        .outerjoin(Cover, Book.cover_id == Cover.id)
        .group_by(Book.id, Book.title, Book.year)
        .order_by(Book.year.desc())
    )

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 9, type=int)
    pagination = books_query.paginate(page=page, per_page=per_page)
    books = pagination.items

    formatted_books = []
    for book in books:
        book = book._asdict()
        book["genres"] = ", ".join([genre for genre in book["genres"].split(",")])
        book["description"] = markdown(book["description"])
        if book["review_status_ids"]:
            book["review_count"] = sum(
                [
                    1
                    for statusId in book["review_status_ids"].split(",")
                    if statusId == "2"
                ]
            ) // len(book["genres"].split(","))
        else:
            book["review_count"] = 0
        if book["review_count"] != 0:
            book["rating"] = (
                sum(
                    [
                        int(rating)
                        for rating, statusId in zip(
                            book["review_rating"].split(","),
                            book["review_status_ids"].split(","),
                        )
                        if statusId == "2"
                    ]
                )
                // len(book["genres"].split(","))
                / book["review_count"]
            )
        else:
            book["rating"] = 0
        formatted_books.append(book)

    return render_template(
        "book/index.html", books=formatted_books, pagination=pagination
    )


@bp.route("/create", methods=["GET", "POST"])
@check_rights("createBook")
@login_required
def create_book():
    # Getting genres from DB
    try:
        genres = db.session.execute(db.select(Genre)).scalars()
    except Exception as e:
        flash(
            f"Возникла ошибка при получении списка жанров из БД. ({e})",
            "danger",
        )
        return redirect(url_for("book.index"))

    # rendering form
    if request.method == "GET":
        return render_template(
            "book/create.html", book={}, genres=genres, selected_genres=[]
        )

    # Saving book
    file = request.files.get("cover")
    cover = None
    book = Book()
    selected_genres = list(map(int, request.form.getlist("genres")))
    try:
        book = Book(**params())
        book.description = clean(request.form.get("description", ""))

        if file.mimetype not in ["image/jpeg", "image/png"]:
            flash("Формат изображения должен быть JPEG или PNG", "danger")
            return render_template(
                "book/create.html",
                book=book,
                genres=genres,
                selected_genres=selected_genres,
            )
        if file and file.filename:
            cover = CoverSaver(file).save()

        cover_id = cover.id if cover else None
        book.cover_id = cover_id

        db.session.add(book)
        db.session.commit()

        for genre in selected_genres:
            db.session.add(GenreToBook(book_id=book.id, genre_id=genre))

        db.session.commit()
    except Exception as e:
        flash(
            f"При сохранении данных возникла ошибка. Проверьте корректность введённых данных. ({e})",
            "danger",
        )
        db.session.rollback()
        return render_template(
            "book/create.html",
            book=book,
            genres=genres,
            selected_genres=selected_genres,
        )

    flash(f"Книга «{book.title}» была успешно добавлена!", "success")

    return redirect(url_for("book.show_book", id=book.id))


@bp.route("/show/<int:id>")
def show_book(id):
    try:
        book = (
            db.session.query(
                Book.id.label("id"),
                Book.title.label("title"),
                Book.description.label("description"),
                Book.author.label("author"),
                Book.publisher.label("publisher"),
                Book.length.label("length"),
                func.group_concat(Genre.name.distinct()).label("genres"),
                Book.year.label("year"),
                func.group_concat(Review.rating).label("review_rating"),
                func.group_concat(Review.status_id).label("review_status_ids"),
                Cover.filename.label("cover_filename"),
            )
            .outerjoin(GenreToBook, Book.id == GenreToBook.book_id)
            .outerjoin(Genre, Genre.id == GenreToBook.genre_id)
            .outerjoin(Review, Book.id == Review.book_id)
            .outerjoin(Cover, Book.cover_id == Cover.id)
            .filter(Book.id == id)
            .group_by(Book.id, Book.title, Book.year)
        ).one()

        book = book._asdict()
        book["genres"] = ", ".join([genre for genre in book["genres"].split(",")])
        book["description"] = markdown(book["description"])
        if book["review_status_ids"]:
            book["review_count"] = sum(
                [
                    1
                    for statusId in book["review_status_ids"].split(",")
                    if statusId == "2"
                ]
            ) // len(book["genres"].split(","))
        else:
            book["review_count"] = 0
        if book["review_count"] != 0:
            book["rating"] = (
                sum(
                    [
                        int(rating)
                        for rating, statusId in zip(
                            book["review_rating"].split(","),
                            book["review_status_ids"].split(","),
                        )
                        if statusId == "2"
                    ]
                )
                // len(book["genres"].split(","))
                / book["review_count"]
            )
        else:
            book["rating"] = 0

        default_review_querry = (
            db.session.query(
                Review.id.label("id"),
                Review.rating.label("rating"),
                Review.text.label("text"),
                Review.created_at.label("created_at"),
                Review.user_id.label("user_id"),
                Review.book_id.label("book_id"),
                # Костыль 'property' (full_name) object has no attribute 'label'
                func.concat(
                    User.last_name,
                    " ",
                    User.first_name,
                    " ",
                    func.ifnull(User.middle_name, ""),
                ).label("username"),
            )
            .outerjoin(User, User.id == Review.user_id)
            .order_by(Review.created_at.desc())
            .filter(Review.status_id == 2)
        )

        if current_user.is_authenticated:
            reviews = (
                default_review_querry.filter(
                    and_(Review.book_id == id, Review.user_id != current_user.id)
                )
            ).all()
            try:
                self_review = (
                    default_review_querry.filter(
                        and_(Review.book_id == id, Review.user_id == current_user.id)
                    )
                ).one()
            except Exception:
                self_review = None
        else:
            reviews = (default_review_querry.filter(Review.book_id == id)).all()
            self_review = None

        formatted_reviews = []
        if reviews:
            for review in reviews:
                review = review._asdict()
                review["text"] = markdown(review["text"])
                formatted_reviews.append(review)

        if self_review:
            self_review = self_review._asdict()
            self_review["text"] = markdown(self_review["text"])

        return render_template(
            "book/show.html",
            book=book,
            reviews=formatted_reviews,
            self_review=self_review,
        )
    except Exception as e:
        flash(f"Возникла ошибка при получении данных из БД. ({e})", "danger")
        return redirect(url_for("book.index"))


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@check_rights("editBook")
@login_required
def edit_book(id):
    try:
        genres = db.session.execute(db.select(Genre)).scalars()
    except Exception as e:
        flash(
            f"Возникла ошибка при получении списка жанров из БД. ({e})",
            "danger",
        )
        return redirect(url_for("book.index"))

    if request.method == "POST":
        book = db.session.query(Book).filter(Book.id == id).one()
        selected_genres = list(map(int, request.form.getlist("genres")))
        try:
            for param in BOOK_PARAMS:
                setattr(book, param, request.form.get(param))
            book.description = clean(request.form.get("description", ""))
            db.session.commit()

            db.session.query(GenreToBook).filter(
                GenreToBook.book_id == book.id
            ).delete()
            for genre in selected_genres:
                db.session.add(GenreToBook(book_id=book.id, genre_id=genre))
            db.session.commit()
        except Exception as e:
            flash(
                f"При сохранении данных возникла ошибка. Проверьте корректность введённых данных. ({e})",
                "danger",
            )
            db.session.rollback()
            return render_template(
                "book/create.html",
                book=book,
                genres=genres,
                selected_genres=selected_genres,
            )

        flash(f"Книга «{book.title}» была успешно изменена!", "success")
        return redirect(url_for("book.index"))

    try:
        book = (
            db.session.query(
                Book.id.label("id"),
                Book.title.label("title"),
                Book.description.label("description"),
                Book.author.label("author"),
                Book.publisher.label("publisher"),
                Book.length.label("length"),
                func.group_concat(Genre.id.distinct()).label("genre_ids"),
                Book.year.label("year"),
                func.coalesce(func.avg(Review.rating), 0).label("rating"),
                func.count(Review.id).label("review_count"),
                Cover.filename.label("cover_filename"),
            )
            .outerjoin(GenreToBook, Book.id == GenreToBook.book_id)
            .outerjoin(Genre, Genre.id == GenreToBook.genre_id)
            .outerjoin(Review, Book.id == Review.book_id)
            .outerjoin(Cover, Book.cover_id == Cover.id)
            .filter(Book.id == id)
            .group_by(Book.id, Book.title, Book.year)
        ).one()
    except Exception:
        flash("Запрошенная книга не существует", "danger")
        return redirect(url_for("book.index"))

    return render_template(
        "book/edit.html",
        book=book,
        genres=genres,
        selected_genres=[int(id) for id in book.genre_ids.split(",")],
    )


@bp.route("/delete/<int:id>")
@check_rights("deleteBook")
@login_required
def delete_book(id):
    try:
        try:
            book = db.session.query(Book).filter(Book.id == id).one()
        except Exception:
            flash("Запрошенная книга не существует", "danger")
            return redirect(url_for("book.index"))

        db.session.delete(book)
        db.session.commit()

        cover = db.session.query(Cover).filter(Cover.id == book.cover_id).one()
        try:
            db.session.delete(cover)
            db.session.commit()
            try:
                CoverRemover(cover.filename).remove()
            except Exception as e:
                flash(
                    f"Возникла ошибка при удалении обложки книги «{book.title}». ({e})",
                    "danger",
                )
                db.session.rollback()
                return redirect(url_for("book.index"))
        except Exception:
            pass

        flash(f"Книга «{book.title}» была успешно удалена!", "success")
        return redirect(url_for("book.index"))
    except Exception:
        flash(f"Возникла ошибка при удалении книги «{book.name}»", "danger")
        db.session.rollback()
        return redirect(url_for("book.index"))


@bp.route("/media/images/<path:filename>")
def media_images(filename):
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "images"),
        filename,
    )
