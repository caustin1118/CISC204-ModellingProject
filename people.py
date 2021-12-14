"""A series of modules containing dictionaries that can be used in run.py"""


def test_person_set_1():
    person1 = {
        "name": "Steven",
        "age": 12,
        "likes": "action",
        "availability": 3
    }

    person2 = {
        "name": "Jane",
        "age": 23,
        "likes": "romance",
        "availability": 2
    }

    person3 = {
        "name": "Alice",
        "age": 18,
        "likes": "romance",
        "availability": 2
    }

    person4 = {
        "name": "Henry",
        "age": 19,
        "likes": "horror",
        "availability": 1
    }

    person5 = {
        "name": "Alex",
        "age": 22,
        "likes": "comedy",
        "availability": 3
    }

    people = [person1, person2, person3, person4, person5]
    return people
