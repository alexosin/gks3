from pulp import *

x1 = LpVariable('x1', 16, cat='Integer')
x2 = LpVariable('x2', 16, cat='Integer')

prob = LpProblem('problem', LpMaximize)

prob += 4*x1+4*x2 <= 166
prob += 5*x1+6*x2 <= 232

prob += 78*x1+90*x2

status = prob.solve()

print(value(x1), value(x2))
