from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

import pprint

# Encoding that will store all of your constraints
E = Encoding()


# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
# Proposition to determine age bracket
@constraint.at_least_one(E)
@proposition(E)
class PersonAgePropositions:
    def __init__(self, ageBracket):
        self.ageBracket = ageBracket

    def __repr__(self):
        return f"PersonAgeBracket.{self.ageBracket}"


L13 = PersonAgePropositions("Less than 13")
L17 = PersonAgePropositions("Less than 17")
A13 = PersonAgePropositions("At least 13")
A17 = PersonAgePropositions("At least 17")


@constraint.at_least_one(E)
@proposition(E)
class PersonPreferencePropositions:
    def __init__(self, favGenre):
        self.favGenre = favGenre

    def __repr__(self):
        return f"PersonPreference.{self.favGenre}"


likesAction = PersonPreferencePropositions("Likes Action")
likesHorror = PersonPreferencePropositions("Horror")
likesRomance = PersonPreferencePropositions("Romance")
likesComedy = PersonPreferencePropositions("Comedy")
likesDocumentary = PersonPreferencePropositions("Documentary")


# Proposition to determine person's availability
@constraint.at_least_one(E)
@proposition(E)
class PersonAvailabilityPropositions:
    def __init__(self, personTime):
        self.personTime = personTime

    def __repr__(self):
        return f"PersonAvailability.{self.personTime}"


L1h = PersonAvailabilityPropositions("Less than 1 hour")
L2h = PersonAvailabilityPropositions("Less than 2 hours")
A1h = PersonAvailabilityPropositions("At least 1 hour")
A2h = PersonAvailabilityPropositions("At least 2 hours")


# Proposition to determine movie rating
@constraint.at_least_one(E)
@proposition(E)
class MovieAgePropositions:
    def __init__(self, rating):
        self.rating = rating

    def __repr__(self):
        return f"MovieRating.{self.rating}"


Rated_G = MovieAgePropositions("Rated G")
Rated_PG13 = MovieAgePropositions("Rated PG13")
Rated_R = MovieAgePropositions("Rated R")


# Proposition to determine movie genre
@constraint.at_least_one(E)
@proposition(E)
class MovieGenreProposition:
    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return f"MovieGenre.{self.genre}"


isAction = MovieGenreProposition("Action")
isHorror = MovieGenreProposition("Horror")
isRomance = MovieGenreProposition("Romance")
isComedy = MovieGenreProposition("Comedy")
isDocumentary = MovieGenreProposition("Documentary")


# Proposition to determine movie length
@constraint.at_least_one(E)
@proposition(E)
class MovieLengthProposition:
    def __init__(self, length):
        self.length = length

    def __repr__(self):
        return f"MovieLength.{self.length}"


MA1h = MovieLengthProposition("Movie is at least 1 hour long")
MA2h = MovieLengthProposition("Movie is at least 2 hours long")


# Proposition to determine if the movie is age appropriate
@proposition(E)
class AgeAppropriateProposition:
    def __init__(self, isAppropriate):
        self.isAppropriate = isAppropriate

    def __repr__(self):
        return f"Appropriate.{self.isAppropriate}"


AgeAppropriate = AgeAppropriateProposition("Age Appropriate")


# Proposition to determine if the movie is likeable
@proposition(E)
class LikeableProposition:
    def __init__(self, isLikeable):
        self.isAppropriate = isLikeable

    def __repr__(self):
        return f"Appropriate.{self.isLikeable}"


likeable = LikeableProposition("Likeable")


# Proposition to determine if the movie is the right length for the people watching
@proposition(E)
class EnoughTimeProposition:
    def __init__(self, enoughTime):
        self.enoughTime = enoughTime

    def __repr__(self):
        return f"EnoughTime.{self.enoughTime}"


enoughTime = EnoughTimeProposition("Enough Time to Watch")


def example_theory():
    # Determining age range
    E.add_constraint(L13 >> L17)
    E.add_constraint(A17 >> A13)
    # Not Appropriate
    E.add_constraint(L13 & Rated_R >> ~AgeAppropriate)
    E.add_constraint(L13 & Rated_PG13 >> ~AgeAppropriate)
    E.add_constraint(L17 & Rated_R >> ~AgeAppropriate)
    # Appropriate
    # G
    E.add_constraint(L13 & Rated_G >> AgeAppropriate)
    E.add_constraint(A13 & Rated_G >> AgeAppropriate)
    # PG13
    E.add_constraint(A13 & Rated_PG13 >> AgeAppropriate)
    # R
    E.add_constraint(A17 & Rated_R >> AgeAppropriate)

    # Determining Appropriate Genre
    # Determining Genre
    E.add_constraint(isAction >> ~(isHorror | isRomance | isComedy | isDocumentary))
    E.add_constraint(isHorror >> ~(isAction | isRomance | isComedy | isDocumentary))
    E.add_constraint(isRomance >> ~(isHorror | isAction | isComedy | isDocumentary))
    E.add_constraint(isComedy >> ~(isHorror | isRomance | isAction | isDocumentary))
    E.add_constraint(isDocumentary >> ~(isHorror | isRomance | isComedy | isAction))
    # Determining Likes
    E.add_constraint(likesDocumentary >> ~(likesHorror | likesRomance | likesComedy | likesAction))
    E.add_constraint(likesHorror >> ~(likesDocumentary | likesRomance | likesComedy | likesAction))
    E.add_constraint(likesRomance >> ~(likesDocumentary | likesHorror | likesComedy | likesAction))
    E.add_constraint(likesComedy >> ~(likesDocumentary | likesRomance | likesHorror | likesAction))
    E.add_constraint(likesAction >> ~(likesDocumentary | likesRomance | likesComedy | likesHorror))
    # Determining likeable genre
    E.add_constraint(likesAction & isAction >> likeable)
    E.add_constraint(likesHorror & isHorror >> likeable)
    E.add_constraint(likesRomance & isRomance >> likeable)
    E.add_constraint(likesComedy & isComedy >> likeable)
    E.add_constraint(likesDocumentary & isDocumentary >> likeable)

    # Determining time
    E.add_constraint(L1h >> L2h)
    E.add_constraint(A2h >> A1h)
    E.add_constraint(L1h & MA2h >> ~enoughTime)
    E.add_constraint(L1h & MA1h >> ~enoughTime)
    E.add_constraint(L2h & MA2h >> ~enoughTime)
    E.add_constraint(A1h & MA1h >> enoughTime)
    E.add_constraint(A2h & MA2h >> enoughTime)
    E.add_constraint(A2h & MA1h >> enoughTime)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())
    print()
