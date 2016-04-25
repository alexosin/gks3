from pulp import *

x1 = LpVariable('x1', 16)
x2 = LpVariable('x2', 16)

prob = LpProblem('problem', LpMaximize)

prob += 4*x1+4*x2 <= 166
prob += 5*x1+6*x2 <= 232

prob += 78*x1+90*x2

status = prob.solve(GLPK(path='C:/Users/Oleksandr/Desktop/winglpk-4.59/glpk-4.59/w32/glpsol.exe', msg=0))

print(value(x1), value(x2))
