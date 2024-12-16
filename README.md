
# Book Management System

A Flask-based web application for managing a collection of books and authors. This system allows users to:

- Add authors and books
- View book details
- Search books by title
- Sort books by author name or title (ascending/descending)
- Delete authors and books

## Features

- **Add Author**: Add a new author with their name, birth date, and date of death (optional).
- **Add Book**: Add a new book with its title, ISBN, publication year, and author.
- **View Book Details**: View the details of a book along with its author.
- **Search Books**: Search for books by title.
- **Sort Books**: Sort books by author name or title in ascending or descending order.
- **Delete Books & Authors**: Delete books or authors from the system.

## Technologies Used

- Python
- Flask
- SQLAlchemy (for database management)
- SQLite (database)
- Marshmallow (for serialization)
- Open Library API (for book cover retrieval)

## Setup Instructions

### Prerequisites

1. Python 3.x
2. pip (Python package installer)

### Install Dependencies

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone the repository:

    ```bash
    git clone https://github.com/masterschool-weiterbildung/weiterbildung-book-alchemy.git
    cd weiterbildung-book-alchemy
    ```

2. Create and initialize the database

3. Start the Flask development server:

    ```bash
    python app.py
    ```

    The application will run at `http://127.0.0.1:5000/`.

## API Documentation

The following endpoints are available:

- **GET /book/<book_id>/details**: Fetch the details of a book by its ID.
- **POST /search**: Search for books by title.
- **GET /home**: View the list of books, optionally sorted by author or title.
- **POST /add_author**: Add a new author.
- **POST /add_book**: Add a new book.
- **GET /book/<book_id>/delete**: Delete a book by its ID.
- **GET /author/<author_id>/delete**: Delete an author by their ID.

