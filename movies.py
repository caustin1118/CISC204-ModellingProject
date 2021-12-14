"""A series of modules containing dictionaries that can be used in run.py"""


def test_movie_set_1():
    movie1 = {
        "name": "Apollo11",
        "rating": "G",
        "genre": "documentary",
        "length": 93
    }
    movie2 = {
        "name": "Cars",
        "rating": "G",
        "genre": "comedy",
        "length": 117
    }
    movie3 = {
        "name": "Pride and Prejudice",
        "rating": "PG13",
        "genre": "romance",
        "length": 135
    }
    movie4 = {
        "name": "Avengers: Infinity War",
        "rating": "PG13",
        "genre": "action",
        "length": 149
    }
    movie5 = {
        "name": "The Conjuring",
        "rating": "R",
        "genre": "horror",
        "length": 112
    }

    movies = [movie1, movie2, movie3, movie4, movie5]
    return movies
