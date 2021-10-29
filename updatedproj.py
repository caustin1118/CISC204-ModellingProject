
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
    E.add_constraint(L13 >> L17);
    E.add_constraint(A17 >> A13);
    #Not Appropriate
    E.add_constraint(L13 & rated_r >> age_appropriate);
    E.add_constraint(L13 & rated_pg13 >> ~age_appropriate);
    E.add_constraint(L17 & rated_r >> ~age_appropriate);
    # Appropriate

        #g
    E.add_constraint(L13 & rated_g >> age_appropriate);
    E.add_constraint(A13 & rated_g >> age_appropriate);
        #pg13

    E.add_constraint(A13 & rated_pg13 >> age_appropriate);
        #R

    E.add_constraint(A17 & rated_r >> age_appropriate)

    #Determining Appropriate genre
    #Determining genre
    E.add_constraint(is_action >> ~(is_horror | is_romance | is_comedy | is_documentary));
    E.add_constraint(is_horror >> ~(is_action | is_romance | is_comedy | is_documentary));
    E.add_constraint(is_romance >> ~(is_horror | is_action | is_comedy | is_documentary));
    E.add_constraint(is_comedy >> ~(is_horror | is_romance | is_action | is_documentary));
    E.add_constraint(is_documentary >> ~(is_horror | is_romance | is_comedy | is_action));
    #Determining Likes
    E.add_constraint(likes_documentary >> ~(likes_horror | likes_romance | likes_comedy | likes_action));
    E.add_constraint(likes_horror >> ~(likes_documentary | likes_romance | likes_comedy | likes_action));
    E.add_constraint(likes_romance >> ~(likes_documentary | likes_horror | likes_comedy | likes_action));
    E.add_constraint(likes_comedy >> ~(likes_documentary | likes_romance | likes_horror | likes_action));
    E.add_constraint(likes_action >> ~(likes_documentary | likes_romance | likes_comedy | likes_horror));
    #Determining likeable genre

    E.add_constraint(likes_action & is_action >> likeable);
    E.add_constraint(likes_horror & is_horror >> likeable);
    E.add_constraint(likes_romance & is_romance >> likeable);
    E.add_constraint(likes_comedy & is_comedy >> likeable);
    E.add_constraint(Likes_documentary & is_documentary >> likeable);

    action, horror, romance, comedy, documentary

    #Determining time
    E.add_constraint(L1 >> L2)
    E.add_constraint(A2 >> A1)
    # Not Appropriate
    E.add_constraint(L1 & g2 >> ~inTime;
    E.add_constraint(L1 & g1 >> ~inTime);
    E.add_constraint(L2 & g2 >> ~inTime);
     #inTime
     g1
    E.add_constraint(A1 & g1 >> inTime);
        #pg13

    E.add_constraint(A2 & g2 >> inTime);
        #R

    E.add_constraint(A2 & g1 >> inTime);


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
