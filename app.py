"""
This script defines a Flask-based web application for managing books.

Key Features:
1. View Details: Retrieve details of a specific book and its associated
   author.
2. Search: Search books by title.
3. Home Page: View and sort the list of books by title or author,
   in ascending or descending order.
4. Add Author: Add new authors with name, birthdate, and (optional) date
   of death.
5. Add Book: Add new books with title, author, ISBN, and publication year.
6. Delete Book: Remove a book from the database using its ID.
7. Delete Author: Remove an author and their books from the database
   using their ID.

"""

from pathlib import Path

from marshmallow import Schema, fields
from flask import Flask, request, render_template

from data_models import db, Author
from crud_util import author_add, book_add, book_delete, get_book, get_author, \
    author_delete
from query_util import search_book, sort_author_asc, sort_author_desc, \
    sort_title_asc, sort_title_desc, fetch_without_order

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{Path(__file__).parent}/"
                                  f"data/library.sqlite3")

db.init_app(app)


class ItemSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)


schema = ItemSchema()

# Sorting and Direction of Post
DIRECTION_ASC = "asc"
DIRECTION_DESC = "desc"

TITLE = "title"
AUTHOR = "author"


@app.route('/book/<int:book_id>/details', methods=['GET'])
def get_details(book_id: int):
    """
    Retrieve and display details of a specific book and its author.

    Parameter:
        book_id (int): The unique identifier of the book.

    Returns:
        Response: Renders the 'get_book_details.html' template with:
            - book: The book object retrieved using the given book ID.
            - author: The author object associated with the book.
    """
    book = get_book(db, book_id)

    author = get_author(db, book.author_id)

    return render_template('get_book_details.html', book=book,
                           author=author)


@app.route('/search', methods=['POST'])
def search():
    """
    Search for books by title and display the results.

    Retrieves books with titles matching the search query (case-insensitive)
    and displays them on the home page.

    Parameter:
        title (str): The search query for the book title, retrieved from the
                     form data.

    Returns:
        Response: Renders the 'home.html' template with:
            - authors_of_books: List of authors and books matching the query.
            - success_search: Boolean indicating whether the search returned
                                results.
    """

    title = request.form.get("title")

    title = f"%{str(title).lower()}%"  # Used for SQL LIKE statement where
    # % is used as wildcards

    authors_of_books = search_book(db, title)

    if not authors_of_books:
        return render_template('home.html',
                               authors_of_books=authors_of_books,
                               success_search=False)

    return render_template('home.html',
                           authors_of_books=authors_of_books)


@app.route('/', methods=['GET'])
def home():
    """
    Display the home page with a list of books and sorting options.

    Parameters:
        sort (str): Sorting criterion, either 'title' or 'author'.
        direction (str): Sorting direction, either 'asc' or 'desc'.

    Returns:
        Response: Renders the 'home.html' template with:
            - authors_of_books: List of authors and their books.
            - sort: The selected sorting criterion (if provided).
            - direction: The selected sorting direction (if provided).
    """

    options_directions = [DIRECTION_ASC, DIRECTION_DESC]
    options_sort = [TITLE, AUTHOR]

    sort = request.args.get('sort')  # Query parameter sort
    direction = request.args.get('direction')  # Query parameter direction

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
    """
    Add a new author to the database.

    Handles both GET and POST requests:
    - GET: Displays the form to add a new author.
    - POST: Processes the submitted form data to add the author.

    Parameters:
        name (str): The name of the author.
        birthdate (str): The birthdate of the author.
        date_of_death (str): The date of death of the author (optional).

    Returns:
        Response:
            - For GET requests, renders the 'add_author.html' template.
            - For POST requests:
                - On success, renders 'add_author.html' with success=True.
                - On failure, renders 'add_author.html' with success=False.
    """

    if request.method == 'POST':
        try:
            name = request.form.get("name")
            birthdate = request.form.get("birthdate")
            date_of_death = request.form.get("date_of_death")

            author_add(db, birthdate, date_of_death, name)

            return render_template('add_author.html',
                                   success=True)
        except  Exception as e:
            print(e)
            return render_template('add_author.html',
                                   success=False)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the database.

    Handles both GET and POST requests:
    - GET: Displays the form to add a new book, including a list of authors.
    - POST: Processes the submitted form data to add the book to the database.

    Parameters:
        author_id (int): The ID of the author for the book.
        isbn (str): The ISBN of the book.
        title (str): The title of the book.
        publication_year (int): The publication year of the book.

    Returns:
        Response:
            - For GET requests, renders the 'add_book.html' template with a
              list of authors.
            - For POST requests:
                - On success, renders 'add_book.html' with success=True
                  and a list of authors.
                - On failure, renders 'add_book.html' with success=False
                  and a list of authors.
    """

    list_of_authors = db.session.execute(
        db.select(Author).order_by(Author.name)).scalars()

    if request.method == 'POST':
        try:
            author_id = request.form.get("author_id")
            isbn = request.form.get("isbn")
            title = request.form.get("title")
            publication_year = request.form.get("publication_year")

            book_add(db, author_id, isbn, publication_year, title)

            return render_template('add_book.html',
                                   success=True,
                                   authors=list_of_authors)
        except  Exception as e:
            print(e)
            return render_template('add_book.html',
                                   success=False,
                                   authors=list_of_authors)

    return render_template('add_book.html',
                           authors=list_of_authors)


@app.route('/book/<int:book_id>/delete')
def delete_book(book_id):
    """
    Delete a specific book from the database.

    Parameter:
        book_id (int): The ID of the book to be deleted.

    Returns:
        Response:
            - Renders 'home.html' with authors_of_books and success=True
              if the deletion is successful.
            - Renders 'home.html' with authors_of_books and success=False
              if an error occurs during deletion.
            - Returns a 404 error if the book ID is not provided.
    """

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


@app.route('/author/<int:author_id>/delete')
def delete_author(author_id):
    """
    Delete a specific author and their associated books from the database.

    Parameter:
        author_id (int): The ID of the author to be deleted.

    Returns:
        Response:
            - Renders 'home.html' with authors_of_books and success_author=True
              if the deletion is successful.
            - Renders 'home.html' with authors_of_books and success_author=False
              if an error occurs during deletion.
            - Returns a 404 error if the author ID is not provided.
    """

    if author_id is None:
        return "Author ID not found", 404

    authors_of_books = fetch_without_order(db)

    try:
        author_delete(db, author_id)

        return render_template('home.html',
                               authors_of_books=authors_of_books,
                               success_author=True)

    except Exception as e:
        print(e)
        return render_template('home.html',
                               authors_of_books=authors_of_books,
                               success_author=False)


if __name__ == '__main__':
    """
    with app.app_context():
    db.create_all()
    """
    app.run(host="0.0.0.0", port=5002, debug=True)
