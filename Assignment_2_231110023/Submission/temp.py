from z3 import *

s = Solver()
x = Int('x')
y = Int('y')
c1 = Int('c1')
c2 = Int('c2')
o1 = Int('o1')

o2 = Int('o2')

mapping = {chr(i): f'o{i-96}' for i in range(97, 123)}
print("mapping", mapping)
s.add(And(Implies(And(And(True, x == 5), y == 100),
        And(And(And(True,
                    Implies(And(And(True, x <= 42),
                                Not(False)),
                            And(And(True, o2 == x),
                                        o1 == x + c1))),
                Implies(And(True, Not(x <= 42)),
                        And(And(True, o2 == x),
                                    o1 == x + c2))),
            And(And(True, o1 == 45), o2 == 5)))),
(Implies(And(And(True, x == 43), y == 100)
            ,
        And(And(And(True,
                    Implies(And(And(True, x <= 42),
                                Not(False)),
                            And(And(And(And(True, o2 == x),
                                        o1 == x + c1),
                                    ),
                                ))),
                Implies(And(True, Not(x <= 42)),
                        And(And(And(And(True, o2 == x),
                                    o1 == x + c2),
                                ),
                            ))),
            And(And(True, o1 == 65), o2 == 43)))))


# s.add(And(True,
#         Implies(And(x == 100, y == 100),
#                 And(And(And(True,
#                             Implies(And(Not(x <= 42)),
#                                     And(And(And(True,
#                                         o1 == x),
#                                         o2 == x + c2)))),
#                         Implies(And(x <= 42),
#                                 And(And(And(True, o1 == x),
#                                         o2 == x + c1 + c2)))),
#                     And(o1 == 100, o2 == 122)))),
#     Implies(And(x == 42, y == 100),
#             And(And(And(True,
#                         Implies(And(Not(x <= 42)),
#                                 And(And(And(True, o1 == x),
#                                         o2 == x + c2)))),
#                     Implies(And(x <= 42),
#                             And(And(And(True, o1 == x),
#                                     o2 == x + c1 + c2)))),
#                 And(o1 == 42, o2 == 82))))
result = s.check()

if result == sat:
    # If the formula is satisfiable, retrieve the satisfying model
    model = s.model()
    x_value = model[x]
    y_value = model[y]
    c1_value = model[c1]
    c2_value = model[c2]

    print("Satisfying values:")
    print("x =", x_value)
    print("y =", y_value)
    print("c1 =", c1_value)
    print("c2 =", c2_value)
else:
    # If the formula is unsatisfiable, no satisfying values exist
    print("No satisfying values found.")