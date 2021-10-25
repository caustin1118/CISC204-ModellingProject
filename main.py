
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = BasicPropositions("LH")
b = BasicPropositions("LR")
c = BasicPropositions("17")
d = BasicPropositions("1H")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created.

    #Determining age range
    E.add_constraint(L13 >> L17)
    E.add_constraint(A17 >> A13)
    #Not Appropriate
    E.add_constraint(L13 & Rated_R >> ~Age Appropriate)
    E.add_constraint(L13 & Rated_PG13 >> ~Age Appropriate)
    E.add_constraint(L17 & Rated_R >> ~Age Appropriate)
    # Appropriate

        #G
    E.add_constraint(L13 & Rated_G >> Age Appropriate)
    E.add_constraint(A13 & Rated_G >> AgeAppropriate)
        #PG13

    E.add_constraint(A13 & Rated_PG13 >> Age Appropriate)
        #R

    E.add_constraint(A17 & Rated_R >> AgeAppropriate)

    #Determining Appropriate Genre
    #Determining Genre
    E.add_constraint(IsAction >> ~(isHorror | isRomance | isComedy | isDocumentary))
    E.add_constraint(IsHorror >> ~(isAction | isRomance | isComedy | isDocumentary))
    E.add_constraint(IsRomance >> ~(isHorror | isAction | isComedy | isDocumentary))
    E.add_constraint(IsComedy >> ~(isHorror | isRomance | isAction | isDocumentary))
    E.add_constraint(IsDocumentary >> ~(isHorror | isRomance | isComedy | isAction))
    #Determining Likes
    E.add_constraint(Likes_Documentary >> ~(Likes_Horror | Likes_Romance | Likes_Comedy | Likes_Action))
    E.add_constraint(Likes_Horror >> ~(Likes_Documentary | Likes_Romance | Likes_Comedy | Likes_Action))
    E.add_constraint(Likes_Romance >> ~(Likes_Documentary | Likes_Horror | Likes_Comedy | Likes_Action))
    E.add_constraint(Likes_Comedy >> ~(Likes_Documentary | Likes_Romance | Likes_Horror | Likes_Action))
    E.add_constraint(Likes_Action >> ~(Likes_Documentary | Likes_Romance | Likes_Comedy | Likes_Horror))
    #Determining likeable genre

    E.add_constraint(Likes_Action & IsAction >> likeable)
    E.add_constraint(Likes_Horror & IsHorror >> likeable)
    E.add_constraint(Likes_Romance & IsRomance >> likeable)
    E.add_constraint(Likes_Comedy & IsComedy >> likeable)
    E.add_constraint(Likes_Documentary & IsDocumentary >> likeable)

    Action, Horror, Romance, Comedy, Documentary

    #Determining time
    E.add_constraint(L1h >> L2H)
    E.add_constraint(A2H >> A1H)
    # Not Appropriate
    E.add_constraint(L1H & G2H >> ~inTime
    E.add_constraint(L1H & G1H >> ~inTime)
    E.add_constraint(L2H & G2H >> ~inTime)
     #inTime
     G1H
    E.add_constraint(A1H & G1H >> inTime)
        #PG13

    E.add_constraint(A2H & G2H >> inTime)
        #R

    E.add_constraint(A2H & G1H >> inTime)


    # Negate a formula
    E.add_constraint((x & y).negate())


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

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
