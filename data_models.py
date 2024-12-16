from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    relationship

"""
Base class for all models in the application.
"""


# https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/
class Base(DeclarativeBase):
    pass


"""
db (SQLAlchemy): The SQLAlchemy instance used for interacting with the database. 
                 It is configured with the Base class as the model class.
"""
db = SQLAlchemy(model_class=Base)


class Author(db.Model):
    """
    Represents an author in the database.

    Attributes:
        id (int): The unique identifier for the author (primary key).
        name (str): The name of the author, must be unique.
        birth_date (date): The birthdate of the author.
        date_of_death (date, optional): The date of death of the author,
                                        can be null.
        books (relationship): A one-to-many relationship to the Book model,
                              where an author can have multiple books.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    birth_date: Mapped[date]
    date_of_death: Mapped[date] = mapped_column(nullable=True)
    books = relationship('Book', backref='Author',
                         cascade='all, delete')

    def __repr__(self):
        return (f"Author(id = {self.id}, "
                f"name = {self.name}, "
                f"birth_date = {self.birth_date}, "
                f"date_of_death = {self.date_of_death})"
                )

    def __str__(self):
        return (f"Author(id = {self.id}, "
                f"name = {self.name}, "
                f"birth_date = {self.birth_date}, "
                f"date_of_death = {self.date_of_death})"
                )


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (int): The unique identifier for the book (primary key).
        author_id (int): The ID of the author associated with the book
                         (foreign key to Author).
        isbn (str): The ISBN of the book, must be unique.
        title (str): The title of the book.
        cover (str): The URL or path to the book's cover image.
        publication_year (date, optional): The publication year of the book,
                                           can be null.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    isbn: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    cover: Mapped[str]
    publication_year: Mapped[date] = mapped_column(nullable=True)

    def __repr__(self):
        return (f"Book(id = {self.id}, "
                f"author_id = {self.author_id}, "
                f"isbn = {self.isbn}, "
                f"title = {self.title}, "
                f"publication_year = {self.publication_year})"
                )

    def __str__(self):
        return (f"Book(id = {self.id}, "
                f"author_id = {self.author_id}, "
                f"isbn = {self.isbn}, "
                f"title = {self.title}, "
                f"publication_year = {self.publication_year})"
                )
