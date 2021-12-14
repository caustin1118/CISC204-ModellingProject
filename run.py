from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions
from people import test_person_set_1
from movies import test_movie_set_1


""" NAVIGATION:
general_prop_constraints (lines 20 - 261): where most of the propositions are.
basic_model (lines 274 - 413): our initial model, tests constraints w/o the group factor.
five_profile_model (lines 429 - ): explores finding a the best movie choice for a group of 5 people.
display_solution (lines): displays the solution in a way that is appropriate for this problem.
**main starts line** """


E = Encoding()

"""Creates the general propositions used for every model regardless of complexity. Propositions are split up by 
category, and whether it is representing a person or a movie. """


def general_prop_creation(age_bracket, genres, lengths, ratings, people, movies):
    # Propositions representing age bracket
    @proposition(E)
    class AgeBracketPropositions:
        def __init__(self, person, age_bracket):
            self.person = person
            self.age_bracket = age_bracket

        def get_person(self):
            return self.person

        def get_age(self):
            return self.age_bracket

        def __repr__(self):
            return f"{self.person} age bracket = {self.age_bracket}"

    ages = {a: [{} for _ in range(len(people))] for a in age_bracket}
    for i in range(len(people)):
        person = people[i]
        for age in age_bracket:
            prop = AgeBracketPropositions(person["name"], age)
            ages[age][i] = prop

    # Propositions representing person preference
    @proposition(E)
    class PersonPreferencePropositions:
        def __init__(self, person, preference):
            self.person = person
            self.preference = preference

        def get_person(self):
            return self.person

        def get_preference(self):
            return self.preference

        def __repr__(self):
            return f"{self.person} preference = {self.preference}"

    preferences = {a: [{} for _ in range(len(people))] for a in genres}
    for i in range(len(people)):
        person = people[i]
        for genre in genres:
            prop = PersonPreferencePropositions(person["name"], genre)
            preferences[genre][i] = prop

    # Propositions representing person's availability
    @proposition(E)
    class AvailabilityPropositions:
        def __init__(self, person, availability):
            self.person = person
            self.availability = availability

        def get_person(self):
            return self.person

        def get_availability(self):
            return self.availability

        def __repr__(self):
            return f"{self.person} availability = {self.availability}"

    availabilities = {a: [{} for _ in range(len(people))] for a in lengths}
    for i in range(len(people)):
        person = people[i]
        for length in lengths:
            prop = AvailabilityPropositions(person["name"], length)
            availabilities[length][i] = prop

    # Propositions representing movie rating
    @proposition(E)
    class MovieRatingPropositions:
        def __init__(self, movie, rating):
            self.movie = movie
            self.rating = rating

        def get_rating(self):
            return self.rating

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.movie} rating = {self.rating}"

    movie_ages = {a: [{} for _ in range(len(movies))] for a in ratings}
    for j in range(len(movies)):
        movie = movies[j]
        for rating in ratings:
            prop = MovieRatingPropositions(movie["name"], rating)
            movie_ages[rating][j] = prop

    # Propositions representing movie genre
    @proposition(E)
    class MovieGenrePropositions:
        def __init__(self, movie, genre):
            self.movie = movie
            self.genre = genre

        def get_genre(self):
            return self.genre

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.movie} genre = {self.genre}"

    movie_genres = {a: [{} for _ in range(len(movies))] for a in genres}
    for j in range(len(movies)):
        movie = movies[j]
        for genre in genres:
            prop = MovieGenrePropositions(movie["name"], genre)
            movie_genres[genre][j] = prop

    # Propositions representing movie length
    @proposition(E)
    class MovieLengthPropositions:
        def __init__(self, movie, length):
            self.movie = movie
            self.length = length

        def get_length(self):
            return self.length

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.movie} length = {self.length}"

    movie_lengths = {a: [{} for _ in range(len(movies))] for a in lengths}
    for j in range(len(movies)):
        movie = movies[j]
        for length in lengths:
            prop = MovieLengthPropositions(movie["name"], length)
            movie_lengths[length][j] = prop

    # Proposition to determine if the movie is age appropriate
    @proposition(E)
    class AgeAppropriateProposition:
        def __init__(self, person, movie):
            self.person = person
            self.movie = movie

        def get_person(self):
            return self.person

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.movie} is age appropriate for {self.person}"

    age_appropriate = {a: [{} for _ in range(len(movies))] for a in range(len(people))}

    for i in range(len(people)):
        for j in range(len(movies)):
            person = people[i]
            movie = movies[j]
            prop = AgeAppropriateProposition(person["name"], movie["name"])
            age_appropriate[i][j] = prop

    # Proposition to determine if the movie is likeable
    @proposition(E)
    class LikeableProposition:
        def __init__(self, person, movie):
            self.person = person
            self.movie = movie

        def get_person(self):
            return self.person

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.movie} is likeable for {self.person}"

    likeable = {a: [{} for _ in range(len(movies))] for a in range(len(people))}

    for i in range(len(people)):
        for j in range(len(movies)):
            person = people[i]
            movie = movies[j]
            prop = LikeableProposition(person["name"], movie["name"])
            likeable[i][j] = prop

    # Proposition to determine if the movie is the right length for the people watching
    @proposition(E)
    class EnoughTimeProposition:
        def __init__(self, person, movie):
            self.person = person
            self.movie = movie

        def get_person(self):
            return self.person

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.person} has enough time to watch {self.movie}"

    enough_time = {a: [{} for _ in range(len(movies))] for a in range(len(people))}

    for i in range(len(people)):
        for j in range(len(movies)):
            person = people[i]
            movie = movies[j]
            prop = EnoughTimeProposition(person["name"], movie["name"])
            enough_time[i][j] = prop

    # Proposition to determine if the movie is suitable for a single person
    @proposition(E)
    class suitableMovieProposition:
        def __init__(self, person, movie):
            self.person = person
            self.movie = movie

        def get_person(self):
            return self.person

        def get_movie(self):
            return self.movie

        def __repr__(self):
            return f"{self.movie} is a suitable movie for {self.person} to watch"

    suitable_movie = {a: [{} for _ in range(len(movies))] for a in range(len(people))}

    for i in range(len(people)):
        for j in range(len(movies)):
            person = people[i]
            movie = movies[j]
            prop = suitableMovieProposition(person["name"], movie["name"])
            suitable_movie[i][j] = prop

    props = [ages, preferences, availabilities, movie_ages, movie_genres, movie_lengths, age_appropriate, likeable,
             enough_time, suitable_movie]

    return props


###########
# MODEL 1 #
###########

""" This model tests a single person against two different movies to evaluate which is a suitable movie for the person 
to watch. This is meant to test the effectiveness of the constraints without having to take multiple people into 
account. """


def basic_model():
    # SECTION 1 : VARIABLES
    age_bracket = ["0_12", "13_16", "17+"]
    genres = ["horror", "romance"]
    lengths = ["less_1hr", "1_2_hours", "min_2hr"]
    ratings = ["G", "PG13", "R"]

    # a person is represented as a dictionary of different variables relevant to their movie preferences
    person = {
        "name": "person",
        "age": 17,
        "likes": "romance",
        "availability": 3
    }

    people = [person]

    # a movie is represented a dictionary of different variables that may be relevant to someone choosing a movie
    movie1 = {
        "name": "movie1",
        "rating": "PG13",
        "genre": "romance",
        "length": 120
    }
    movie2 = {
        "name": "movie2",
        "rating": "R",
        "genre": "horror",
        "length": 85
    }

    movies = [movie1, movie2]

    # SECTION 2 : PROPOSITIONS
    props = general_prop_creation(age_bracket, genres, lengths, ratings, people, movies)
    ages = props[0]
    preferences = props[1]
    availabilities = props[2]
    movie_ages = props[3]
    movie_genres = props[4]
    movie_lengths = props[5]
    age_appropriate = props[6]
    likeable = props[7]
    enough_time = props[8]
    suitable_movie = props[9]

    # SECTION 3 : CONSTRAINTS
    personAge = 0
    personAvailable = 0

    # loops through all people. movies
    for i in range(len(movies)):
        for j in range(len(people)):
            if person["age"] < 13:
                constraint.add_exactly_one(E, ages[age_bracket[0]][j])
            elif (person["age"] >= 13) and (person["age"] < 17):
                personAge = 1
                constraint.add_exactly_one(E, ages[age_bracket[1]][j])
            elif person["age"] >= 17:
                personAge = 2
                constraint.add_exactly_one(E, ages[age_bracket[2]][j])

            for genre in genres:
                preference = preferences[genre][j]
                if person["likes"] == preference.get_preference():
                    constraint.add_exactly_one(E, preference)

            if person["availability"] < 1:
                constraint.add_exactly_one(E, availabilities["less_1hr"][j])
            elif 1 <= person["availability"] < 2:
                personAvailable = 1
                constraint.add_exactly_one(E, availabilities["1_2_hours"][j])
            elif person["availability"] >= 2:
                personAvailable = 2
                constraint.add_exactly_one(E, availabilities["min_2hr"][j])

            movie = movies[i]
            person = people[j]
            for rating in ratings:
                movie_age = movie_ages[rating][i]
                if (movie["name"] == movie_age.get_movie()) and (movie["rating"] == movie_age.get_rating()):
                    constraint.add_exactly_one(E, movie_age)
            for genre in genres:
                movie_genre = movie_genres[genre][i]
                if (movie["name"] == movie_genre.get_movie()) and (movie["genre"] == movie_genre.get_genre()):
                    constraint.add_exactly_one(E, movie_genre)

            if (movie["length"] / 60) < 1:
                constraint.add_exactly_one(E, movie_lengths["less_1hr"][i])
            elif 1 <= (movie["length"] / 60) < 2:
                constraint.add_exactly_one(E, movie_lengths["1_2_hours"][i])
            elif (movie["length"] / 60) >= 2:
                constraint.add_exactly_one(E, movie_lengths["min_2hr"][i])

            E.add_constraint(~(ages[age_bracket[0]][j] & (ages[age_bracket[1]][j] | ages[age_bracket[2]][j])))
            E.add_constraint(~(ages[age_bracket[1]][j] & (ages[age_bracket[0]][j] | ages[age_bracket[2]][j])))
            E.add_constraint(~(ages[age_bracket[2]][j] & (ages[age_bracket[0]][j] | ages[age_bracket[1]][j])))

            E.add_constraint(~(movie_ages["G"][i] & (movie_ages["PG13"][i] | movie_ages["R"][i])))
            E.add_constraint(~(movie_ages["PG13"][i] & (movie_ages["G"][i] | movie_ages["R"][i])))
            E.add_constraint(~(movie_ages["R"][i] & (movie_ages["PG13"][i] | movie_ages["G"][i])))

            E.add_constraint(~(preferences["horror"][j] & preferences["romance"][j]))
            E.add_constraint(~(movie_genres["horror"][i] & movie_genres["romance"][i]))

            E.add_constraint(
                ~(movie_lengths["less_1hr"][i] & (movie_lengths["1_2_hours"][i] | movie_lengths["min_2hr"][i])))
            E.add_constraint(
                ~(movie_lengths["1_2_hours"][i] & (movie_lengths["less_1hr"][i] | movie_lengths["min_2hr"][i])))
            E.add_constraint(
                ~(movie_lengths["min_2hr"][i] & (movie_lengths["1_2_hours"][i] | movie_lengths["less_1hr"][i])))

            if personAge == 0:
                E.add_constraint(ages[age_bracket[0]][j] & movie_ages["G"][i] >> age_appropriate[j][i])
            elif personAge == 1:
                E.add_constraint(
                    ages[age_bracket[1]][j] & (movie_ages["G"][i] | movie_ages["PG13"][i]) >> age_appropriate[j][i])
            else:
                E.add_constraint(ages[age_bracket[2]][j] & (movie_ages["G"][i] | movie_ages["PG13"][i] | movie_ages["R"][i]) >>
                                 age_appropriate[j][i])

            E.add_constraint((preferences["horror"][j] & movie_genres["horror"][i]) | (
                    preferences["romance"][j] & movie_genres["romance"][i]) >> likeable[j][i])

            if personAvailable == 0:
                E.add_constraint(availabilities["less_1hr"][j] & movie_lengths["less_1hr"][i] >> enough_time[j][i])
            elif personAvailable == 1:
                E.add_constraint(
                    availabilities["1_2_hours"][j] & (movie_lengths["less_1hr"][i] | movie_lengths["1_2_hours"][i]) >>
                    enough_time[j][i])
            else:
                E.add_constraint(availabilities["min_2hr"][j] & (
                        movie_lengths["less_1hr"][i] | movie_lengths["1_2_hours"][i] | movie_lengths["min_2hr"][i]) >>
                                 enough_time[j][i])

            E.add_constraint((age_appropriate[j][i] & likeable[j][i] & enough_time[j][i]) >> suitable_movie[j][i])

    basic_theory = E.compile()

    return basic_theory


###########
# MODEL 2 #
###########

""" This model tests five people against five different movies to evaluate which is the best movie for the group to 
watch. This approach allows us to test how our propositions and constraints work for determining suitability in a 
group setting. 

DISCLAIMER : this model was never able to be fully completed, but using T.solve() with this model does show some of the 
ways in which you would begin to apply the methods of solving the basic model to a group."""


def five_profile_model():
    # SECTION 1 : VARIABLES
    group_size = 5
    age_bracket = ["0_12", "13_16", "17+"]
    genres = ["action", "comedy", "documentary", "horror", "romance"]
    lengths = ["less_1hr", "1_2_hours", "2_3_hours", "3_4_hours"]
    ratings = ["G", "PG13", "R"]

    # information on people / movies are taken from the people & movies classes for easier access

    people = test_person_set_1()
    movies = test_movie_set_1()

    # SECTION 2 : PROPOSITIONS
    props = general_prop_creation(age_bracket, genres, lengths, ratings, people, movies)
    ages = props[0]
    preferences = props[1]
    availabilities = props[2]
    movie_ages = props[3]
    movie_genres = props[4]
    movie_lengths = props[5]
    age_appropriate = props[6]
    likeable = props[7]
    enough_time = props[8]
    suitable_movie = props[9]

    # SECTION 3 : CONSTRAINTS
    personAge = 0
    personAvailable = 0

    # loops through all people. movies
    for i in range(len(movies)):
        for j in range(len(people)):
            movie = movies[i]
            person = people[j]

            if person["age"] < 13:
                constraint.add_exactly_one(E, ages[age_bracket[0]][j])
            elif (person["age"] >= 13) and (person["age"] < 17):
                personAge = 1
                constraint.add_exactly_one(E, ages[age_bracket[1]][j])
            elif person["age"] >= 17:
                personAge = 2
                constraint.add_exactly_one(E, ages[age_bracket[2]][j])

            for rating in ratings:
                movie_age = movie_ages[rating][i]
                if (movie["name"] == movie_age.get_movie()) and (movie["rating"] == movie_age.get_rating()):
                    constraint.add_exactly_one(E, movie_age)

            for genre in genres:
                preference = preferences[genre][j]
                if person["likes"] == preference.get_preference():
                    constraint.add_exactly_one(E, preference)

                movie_genre = movie_genres[genre][i]
                if (movie["name"] == movie_genre.get_movie()) and (movie["genre"] == movie_genre.get_genre()):
                    constraint.add_exactly_one(E, movie_genre)

            for length in lengths:
                availability = availabilities[length][j]
                if person["availability"] == availability.get_availability():
                    constraint.add_exactly_one(E, availability)

            if (movie["length"] / 60) < 1:
                constraint.add_exactly_one(E, movie_lengths["less_1hr"][i])
            elif 1 <= (movie["length"] / 60) < 2:
                constraint.add_exactly_one(E, movie_lengths["1_2_hours"][i])
            elif 2 <= (movie["length"] / 60) < 3:
                constraint.add_exactly_one(E, movie_lengths["2_3_hours"][i])
            elif 3 <= (movie["length"] / 60) < 4:
                constraint.add_exactly_one(E, movie_lengths["3_4_hours"][i])

            E.add_constraint(~(ages[age_bracket[0]][j] & (ages[age_bracket[1]][j] | ages[age_bracket[2]][j])))
            E.add_constraint(~(ages[age_bracket[1]][j] & (ages[age_bracket[0]][j] | ages[age_bracket[2]][j])))
            E.add_constraint(~(ages[age_bracket[2]][j] & (ages[age_bracket[0]][j] | ages[age_bracket[1]][j])))

            E.add_constraint(~(movie_ages["G"][i] & (movie_ages["PG13"][i] | movie_ages["R"][i])))
            E.add_constraint(~(movie_ages["PG13"][i] & (movie_ages["G"][i] | movie_ages["R"][i])))
            E.add_constraint(~(movie_ages["R"][i] & (movie_ages["PG13"][i] | movie_ages["G"][i])))

            E.add_constraint(~(preferences["action"][j] & (
                        preferences["comedy"][j] | preferences["documentary"][j] | preferences["horror"][j] |
                        preferences["romance"][j])))
            E.add_constraint(~(preferences["comedy"][j] & (
                        preferences["action"][j] | preferences["documentary"][j] | preferences["horror"][j] |
                        preferences["romance"][j])))
            E.add_constraint(~(preferences["documentary"][j] & (
                        preferences["comedy"][j] | preferences["action"][j] | preferences["horror"][j] |
                        preferences["romance"][j])))
            E.add_constraint(~(preferences["horror"][j] & (
                        preferences["comedy"][j] | preferences["documentary"][j] | preferences["action"][j] |
                        preferences["romance"][j])))
            E.add_constraint(~(preferences["romance"][j] & (
                        preferences["comedy"][j] | preferences["documentary"][j] | preferences["horror"][j] |
                        preferences["action"][j])))

            E.add_constraint(~(movie_genres["horror"][i] & movie_genres["romance"][i]))

            E.add_constraint(~(movie_lengths["less_1hr"][i] & (
                        movie_lengths["1_2_hours"][i] | movie_lengths["2_3_hours"][i] | movie_lengths["3_4_hours"][i])))
            E.add_constraint(~(movie_lengths["1_2_hours"][i] & (
                        movie_lengths["less_1hr"][i] | movie_lengths["2_3_hours"][i] | movie_lengths["3_4_hours"][i])))
            E.add_constraint(~(movie_lengths["2_3_hours"][i] & (
                        movie_lengths["1_2_hours"][i] | movie_lengths["less_1hr"][i] | movie_lengths["3_4_hours"][i])))
            E.add_constraint(~(movie_lengths["3_4_hours"][i] & (
                        movie_lengths["1_2_hours"][i] | movie_lengths["less_1hr"][i] | movie_lengths["2_3_hours"][i])))

    five_profile_theory = E.compile()
    return five_profile_theory


def display_solution(mod):
    # basic_model display
    sol = mod.solve()
    for key in sol:
        if "suitable" in str(key):
            if sol[key]:
                movie_name = str(key).split(" ")
                return movie_name[0]

    # five_profile display


if __name__ == "__main__":
    T = basic_model()
    # T = five_profile_model()

    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print(T.solve())
    print("\nBest movie choice: %s" % display_solution(T))
