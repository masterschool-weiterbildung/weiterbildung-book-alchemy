from datetime import datetime
from pathlib import Path

from marshmallow import Schema, fields
from flask import Flask, request, render_template
from sqlalchemy import select, desc, asc, func

from api_util import get_book_cover_from_api
from data_models import db, Author, Book

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

    authors_of_books = db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(Book).join(
            Author, Book.author_id == Author.id).filter(
            func.lower(Book.title).like(title))).all()

    return render_template('home.html', authors_of_books=authors_of_books)


@app.route('/home', methods=['GET'])
def home():
    options_directions = [DIRECTION_ASC, DIRECTION_DESC]
    options_sort = [TITLE, AUTHOR]

    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if sort in options_sort and direction in options_directions:

        if sort == TITLE and direction == DIRECTION_DESC:
            authors_of_books = db.session.execute(
                select(Book.title, Book.cover, Author.name).select_from(
                    Book).join(Author, Book.author_id == Author.id).order_by(
                    desc(Book.title)))

        if sort == TITLE and direction == DIRECTION_ASC:
            authors_of_books = db.session.execute(
                select(Book.title, Book.cover, Author.name).select_from(
                    Book).join(Author, Book.author_id == Author.id).order_by(
                    asc(Book.title)))

        if sort == AUTHOR and direction == DIRECTION_DESC:
            authors_of_books = db.session.execute(
                select(Book.title, Book.cover, Author.name).select_from(
                    Book).join(Author, Book.author_id == Author.id).order_by(
                    desc(Author.name)))

        if sort == AUTHOR and direction == DIRECTION_ASC:
            authors_of_books = db.session.execute(
                select(Book.title, Book.cover, Author.name).select_from(
                    Book).join(Author, Book.author_id == Author.id).order_by(
                    asc(Author.name)))

    else:
        authors_of_books = db.session.execute(
            select(Book.title, Book.cover, Author.name).select_from(
                Book).join(Author, Book.author_id == Author.id))

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

            format = '%Y-%m-%d'

            author = Author()
            author.name = name
            author.birth_date = datetime.strptime(birthdate,
                                                  format).date()
            if date_of_death:
                author.date_of_death = datetime.strptime(date_of_death,
                                                         format).date()

            db.session.add(author)
            db.session.commit()
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

            format = '%Y-%m-%d'

            book = Book()
            book.author_id = author_id
            book.isbn = isbn
            book.title = title
            book.cover = get_book_cover_from_api(isbn)
            book.birth_date = datetime.strptime(publication_year,
                                                format).date()

            db.session.add(book)
            db.session.commit()
            return render_template('add_book.html', success=True,
                                   authors=list_of_authors)
        except  Exception as e:
            print(e)
            return render_template('add_book.html', success=False,
                                   authors=list_of_authors)

    return render_template('add_book.html', authors=list_of_authors)


if __name__ == '__main__':
    """
    with app.app_context():
    db.create_all()
    """
    app.run(host="0.0.0.0", port=5001, debug=True)
