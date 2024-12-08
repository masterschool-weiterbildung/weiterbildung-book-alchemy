from datetime import datetime
from pathlib import Path

from marshmallow import Schema, fields
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import delete

from data_models import db, Author, Book
from crud_util import author_add, book_add, book_delete
from query_util import search_book, sort_author_asc, sort_author_desc, \
    sort_title_asc, sort_title_desc, fetch_without_order

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{Path(__file__).parent}/"
                                  f"data/library.sqlite3")

db.init_app(app)


def jsonify_response(version, payload):
    return {
        "version": version,
        "books": payload,
        "createdAt": datetime.datetime.now().isoformat()
    }


def standard_error_response(status, error, error_code, message, details,
                            path):
    return {
        "status": f"{status}",
        "error": f"{error}",
        "errorCode": f"{error_code}",
        "message": f"{message}",
        "details": f"{details}",
        "path": f"{path}"
    }


class ItemSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)


schema = ItemSchema()

# Sorting and Direction of Post
DIRECTION_ASC = "asc"
DIRECTION_DESC = "desc"

TITLE = "title"
AUTHOR = "author"


@app.route('/search', methods=['POST'])
def search():
    title = request.form.get("title")

    title = f"%{str(title).lower()}%"

    authors_of_books = search_book(db, title)

    return render_template('home.html', authors_of_books=authors_of_books)


@app.route('/home', methods=['GET'])
def home():
    options_directions = [DIRECTION_ASC, DIRECTION_DESC]
    options_sort = [TITLE, AUTHOR]

    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if sort in options_sort and direction in options_directions:

        if sort == TITLE and direction == DIRECTION_DESC:
            authors_of_books = sort_title_desc(db)

        if sort == TITLE and direction == DIRECTION_ASC:
            authors_of_books = sort_title_asc(db)

        if sort == AUTHOR and direction == DIRECTION_DESC:
            authors_of_books = sort_author_desc(db)

        if sort == AUTHOR and direction == DIRECTION_ASC:
            authors_of_books = sort_author_asc(db)

    else:
        authors_of_books = fetch_without_order(db)

    return render_template('home.html',
                           authors_of_books=authors_of_books,
                           sort=sort,
                           direction=direction)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        try:
            name = request.form.get("name")
            birthdate = request.form.get("birthdate")
            date_of_death = request.form.get("date_of_death")

            author_add(db, birthdate, date_of_death, name)

            return render_template('add_author.html', success=True)
        except  Exception as e:
            print(e)
            return render_template('add_author.html', success=False)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    list_of_authors = db.session.execute(
        db.select(Author).order_by(Author.name)).scalars()

    if request.method == 'POST':
        try:
            author_id = request.form.get("author_id")
            isbn = request.form.get("isbn")
            title = request.form.get("title")
            publication_year = request.form.get("publication_year")

            book_add(db, author_id, isbn, publication_year, title)

            return render_template('add_book.html', success=True,
                                   authors=list_of_authors)
        except  Exception as e:
            print(e)
            return render_template('add_book.html', success=False,
                                   authors=list_of_authors)

    return render_template('add_book.html', authors=list_of_authors)


@app.route('/book/<int:book_id>/delete')
def delete_book(book_id):
    if book_id is None:
        return "Book ID not found", 404

    authors_of_books = fetch_without_order(db)

    try:
        book_delete(db, book_id)

        return render_template('home.html',
                               authors_of_books=authors_of_books,
                               success=True)
    except Exception as e:
        print(e)
        return render_template('home.html',
                               authors_of_books=authors_of_books,
                               success=False)


if __name__ == '__main__':
    """
    with app.app_context():
    db.create_all()
    """
    app.run(host="0.0.0.0", port=5001, debug=True)
