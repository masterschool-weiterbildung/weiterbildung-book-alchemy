import json

import requests

MOVIE_API_URL = "https://openlibrary.org/api/books"


def get_parameters(ISBN: str) -> str:
    return f"?bibkeys=ISBN:{ISBN}&format=json&jscmd=data"


def get_book_cover_from_api(ISBN: str) -> json:
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
