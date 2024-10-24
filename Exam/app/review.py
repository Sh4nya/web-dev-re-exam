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
from models import db, Review, Book, ReviewStatus, User
from auth import check_rights
from nh3 import clean
from sqlalchemy.sql import func, and_
from markdown2 import markdown

bp = Blueprint("review", __name__, url_prefix="/review")


@bp.route("/create/<int:book_id>", methods=["GET", "POST"])
@login_required
def create_review(book_id):
    if request.method == "GET":
        try:
            review = (
                db.session.query(Review)
                .filter(
                    and_(Review.user_id == current_user.id, Review.book_id == book_id)
                )
                .one()
            )
            flash("Вы уже оставляли рецензию", "warning")
            return redirect(url_for("book.show_book", id=book_id))
        except Exception:
            pass
        review = Review(book_id=book_id, user_id=current_user.id, rating=5)
        return render_template("review/create.html", review=review)

    review = Review(
        book_id=book_id,
        user_id=current_user.id,
        rating=request.form.get("rating", 5, int),
        text=clean(request.form.get("text", "")),
    )
    try:
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        flash(f"Возникла ошибка при сохранении рецензии. ({e})", "danger")
        return render_template("review/create.html", review=review)

    flash("Рецензия успешно сохранена", "success")
    return redirect(url_for("book.show_book", id=book_id))


@bp.route("/delete/<int:book_id>/<int:review_id>", methods=["GET", "POST"])
@login_required
def delete_review(book_id, review_id):
    review = db.session.query(Review).filter(Review.id == review_id).one()
    if current_user.id != review.user_id:
        flash("У вас нет прав для удаления рецензии", "danger")
        return redirect(url_for("book.show_book", id=book_id))

    review = db.session.query(Review).filter(Review.id == review_id).one()
    try:
        db.session.delete(review)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Возникла ошибка при удалении рецензии. ({e})", "danger")
        return redirect(url_for("book.show_book", id=book_id))

    flash("Рецензия успешно удалена", "success")
    return redirect(url_for("book.show_book", id=book_id))


@bp.route("/my")
@login_required
def my_reviews():
    reviews_query = (
        db.session.query(
            Book.title.label("book_title"),
            Review.rating.label("rating"),
            Review.text.label("text"),
            ReviewStatus.name.label("status"),
        )
        .join(Book, Review.book_id == Book.id)
        .join(ReviewStatus, Review.status_id == ReviewStatus.id)
        .filter(Review.user_id == current_user.id)
    )
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = reviews_query.paginate(page=page, per_page=per_page)
    reviews = pagination.items

    formatted_reviews = []
    for review in reviews:
        review = review._asdict()
        review["text"] = markdown(review["text"])
        formatted_reviews.append(review)

    return render_template(
        "review/my.html", reviews=formatted_reviews, pagination=pagination
    )


@bp.route("/moderate")
@check_rights("moderateReviews")
@login_required
def moderate_reviews():
    reviews_query = (
        db.session.query(
            Book.title.label("book_title"),
            Review.id.label("id"),
            Review.rating.label("rating"),
            Review.text.label("text"),
            Review.created_at.label("created_at"),
            ReviewStatus.name.label("status"),
            func.concat(
                User.last_name,
                " ",
                User.first_name,
                " ",
                func.ifnull(User.middle_name, ""),
            ).label("username"),
        )
        .join(Book, Review.book_id == Book.id)
        .join(ReviewStatus, Review.status_id == ReviewStatus.id)
        .join(User, User.id == Review.user_id)
        .filter(Review.status_id == 1)
        .order_by(Review.created_at)
    )
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = reviews_query.paginate(page=page, per_page=per_page)
    reviews = pagination.items

    formatted_reviews = []
    for review in reviews:
        review = review._asdict()
        review["text"] = markdown(review["text"])
        formatted_reviews.append(review)

    return render_template(
        "review/moderate.html", reviews=formatted_reviews, pagination=pagination
    )


@bp.route("/inspect/<int:review_id>")
@check_rights("moderateReviews")
@login_required
def inspect_review(review_id):
    review = (
        db.session.query(
            Book.title.label("book_title"),
            Review.id.label("id"),
            Review.rating.label("rating"),
            Review.text.label("text"),
            Review.created_at.label("created_at"),
            ReviewStatus.name.label("status"),
            func.concat(
                User.last_name,
                " ",
                User.first_name,
                " ",
                func.ifnull(User.middle_name, ""),
            ).label("username"),
        )
        .join(Book, Review.book_id == Book.id)
        .join(ReviewStatus, Review.status_id == ReviewStatus.id)
        .join(User, User.id == Review.user_id)
        .filter(Review.id == review_id)
        .order_by(Review.created_at)
    ).one()

    review = review._asdict()
    review["text"] = markdown(review["text"])

    return render_template("review/inspect.html", review=review)


@bp.route("/decision/<int:review_id>/<string:status>")
@check_rights("moderateReviews")
@login_required
def decision_review(review_id, status):
    review = db.session.query(Review).filter(Review.id == review_id).one()
    match status:
        case "approve":
            review.status_id = 2
            flash(f"Рецензия №{review.id} одобрена", "success")
        case "reject":
            flash(f"Рецензия №{review.id} отклонена", "success")
            review.status_id = 3
    db.session.commit()

    return redirect(url_for("review.moderate_reviews"))
