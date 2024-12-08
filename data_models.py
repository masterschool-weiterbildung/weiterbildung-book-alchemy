from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    birth_date: Mapped[date]
    date_of_death: Mapped[date] = mapped_column(nullable=True)

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
