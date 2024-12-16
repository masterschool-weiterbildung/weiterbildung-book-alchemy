from sqlalchemy import select, func, asc, desc

from data_models import Book, Author


def search_book(db, title):
    """
    Searches for books by title and returns a list of book details along with author names.

    Parameters:
        db (SQLAlchemy session): The database session used to query the database.
        title (str): The title (or part of the title) of the book to search
                     for. The title is matched case-insensitively using a LIKE query.

    Returns:
        list: A list of tuples containing book details (ID, title, cover)
              and the associated author's name for each book.
    """
    authors_of_books = db.session.execute(
        select(Book.id, Book.title, Book.cover, Author.name).select_from(
            Book).join(
            Author, Book.author_id == Author.id).filter(
            func.lower(Book.title).like(title))).all()
    return authors_of_books


def sort_author_asc(db):
    """
    Retrieves books ordered by author's name in ascending order.

    Parameter:
        db (SQLAlchemy session): The database session used to query the database.

    Returns:
        Result: A SQLAlchemy result object containing a list
                of tuples, each representing a book with
                details (ID, author ID, title, cover)
                and the associated author's name, ordered
                by author's name in ascending order.
    """

    return db.session.execute(
        select(Book.id, Book.author_id, Book.title, Book.cover,
               Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            asc(Author.name)))


def sort_author_desc(db):
    """
    Retrieves books ordered by author's name in descending order.

    Parameter:
        db (SQLAlchemy session): The database session used to query the database.

    Returns:
        Result: A SQLAlchemy result object containing a list of tuples, each
                representing a book with details (ID, author ID, title, cover)
                and the associated author's name, ordered by author's name
                in descending order.
    """

    return db.session.execute(
        select(Book.id, Book.author_id, Book.title, Book.cover,
               Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            desc(Author.name)))


def sort_title_asc(db):
    """
    Retrieves books ordered by title in ascending order.

    Parameter:
        db (SQLAlchemy session): The database session used to query the database.

    Returns:
        Result: A SQLAlchemy result object containing a list of tuples, each
                representing a book with details (ID, author ID, title, cover)
                and the associated author's name, ordered by title in
                ascending order.
    """
    return db.session.execute(
        select(Book.id, Book.author_id, Book.title, Book.cover,
               Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            asc(Book.title)))


def sort_title_desc(db):
    """
    Retrieves books ordered by title in descending order.

    Parameter:
        db (SQLAlchemy session): The database session used to query the database.

    Returns:
        Result: A SQLAlchemy result object containing a list of tuples, each
                representing a book with details (ID, author ID, title, cover)
                and the associated author's name, ordered by title in
                descending order.
    """
    return db.session.execute(
        select(Book.id, Book.author_id, Book.title, Book.cover,
               Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            desc(Book.title)))


def fetch_without_order(db):
    """
    Fetches all books and their authors without any specific order.

    Parameter:
        db (SQLAlchemy session): The database session used to query the database.

    Returns:
        Result: A SQLAlchemy result object containing a list of tuples, each
                representing a book with details (ID, author ID, title, cover)
                and the associated author's name, without any ordering.
    """

    authors_of_books = db.session.execute(
        select(Book.id, Book.author_id, Book.title, Book.cover,
               Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id))
    return authors_of_books
