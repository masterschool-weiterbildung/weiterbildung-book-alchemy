from datetime import datetime

from api_util import get_book_cover_from_api
from data_models import Author, Book


def author_add(db, birthdate, date_of_death, name):
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


def book_add(db, author_id, isbn, publication_year, title):
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
