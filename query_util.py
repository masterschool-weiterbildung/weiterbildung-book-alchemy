from sqlalchemy import select, func, asc, desc

from data_models import Book, Author


def search_book(db, title):
    authors_of_books = db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(Book).join(
            Author, Book.author_id == Author.id).filter(
            func.lower(Book.title).like(title))).all()
    return authors_of_books


def sort_author_asc(db):
    return db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            asc(Author.name)))


def sort_author_desc(db):
    return db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            desc(Author.name)))


def sort_title_asc(db):
    return db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            asc(Book.title)))


def sort_title_desc(db):
    return db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id).order_by(
            desc(Book.title)))


def fetch_without_order(db):
    authors_of_books = db.session.execute(
        select(Book.title, Book.cover, Author.name).select_from(
            Book).join(Author, Book.author_id == Author.id))
    return authors_of_books

