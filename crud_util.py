from datetime import datetime

from api_util import get_book_cover_from_api
from data_models import Author, Book


def author_add(db, birthdate: str, date_of_death: str, name: str):
    """
    Adds a new author to the database.

    Parameters:
        db: The database session object to interact with the database.
        birthdate (str): The birthdate of the author in YYYY-MM-DD format.
        date_of_death (str, optional): The date of death of the author in
                                       YYYY-MM-DD format (optional).
        name (str): The name of the author.

    Returns:
        None
    """

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


def book_add(db, author_id: int, isbn: str, publication_year: str,
             title: str):
    """
    Adds a new book to the database.

    Parameter:
        db: The database session object to interact with the database.
        author_id (int): The ID of the author associated with the book.
        isbn (str): The ISBN of the book.
        publication_year (str): The publication year of the book in 'YYYY-MM-DD' format.
        title (str): The title of the book.

    Returns:
        None
    """

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


def book_delete(db, book_id: int):
    """
    Deletes a book from the database based on its ID.

    Parameters:
        db: The database session object to interact with the database.
        book_id (int): The ID of the book to be deleted.

    Returns:
        None
    """
    book = db.session.get(Book, book_id)
    db.session.delete(book)
    db.session.commit()


def author_delete(db, author_id: int):
    """
    Deletes an author from the database based on their ID.

    Parameters:
        db: The database session object to interact with the database.
        author_id (int): The ID of the author to be deleted.

    Returns:
        None
    """
    author = db.session.get(Author, author_id)
    db.session.delete(author)
    db.session.commit()


def get_book(db, book_id: int):
    """
    Retrieves a book from the database based on its ID.

    Parameters:
        db: The database session object to interact with the database.
        book_id (int): The ID of the book to be retrieved.

    Returns:
        Book: The book object corresponding to the provided ID,
              or None if not found.
    """
    return db.session.get(Book, book_id)


def get_author(db, author_id: int):
    """
    Retrieves an author from the database based on their ID.

    Parameters:
        db: The database session object to interact with the database.
        author_id (int): The ID of the author to be retrieved.

    Returns:
        Author: The author object corresponding to the provided ID,
                or None if not found.
    """
    return db.session.get(Author, author_id)
