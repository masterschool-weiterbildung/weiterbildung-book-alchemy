import json

import requests

"""
The base URL for the Open Library API to fetch the cover images.
"""
MOVIE_API_URL = "https://openlibrary.org/api/books"


def get_parameters(ISBN: str) -> str:
    """
    Generates the query parameters for the Open Library API request based
    on the given ISBN.

    Parameter:
        ISBN (str): The ISBN of the book.

    Returns:
        str: The formatted query string to be used in the API request.
    """

    return f"?bibkeys=ISBN:{ISBN}&format=json&jscmd=data"


def get_book_cover_from_api(ISBN: str) -> json:
    """
    Fetches the cover image URL of a book from the Open Library API based on its ISBN.

    Parameter:
        ISBN (str): The ISBN of the book whose cover image is to be fetched.

    Returns:
        str: The URL of the medium-sized book cover image, if available.
    """

    try:
        response = requests.get(
            MOVIE_API_URL + get_parameters(ISBN),
            verify=True,
            timeout=5)

        response.raise_for_status()

        if response.status_code == 200:
            return response.json()[f"ISBN:{ISBN}"]["cover"]["medium"]
        else:
            print("Status Code returned not 200")

    except requests.exceptions.RequestException as r:
        print(r)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(e)
