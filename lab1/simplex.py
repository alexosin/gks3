from scipy.optimize import linprog
from os import path
from sys import argv
import numpy as np

def print_list(list):
	for i in list:
		print(i)

def cb(xk, **kwargs):
	print('------------------------------------', kwargs.pop('nit'), '------------------------------------')
	print('Ведущий элемент ', kwargs.pop('pivot'))
	print('Индексы столбцов базисных переменных ', kwargs.pop('basis'))
	print('Симплекс таблица\n')
	print_list(kwargs.pop('tableau').tolist())
	print('Решение на данной итерации', xk)
	print('\n\n')

#reading from file
filepath = str(path.realpath(path.dirname(argv[0]))) + '\data.txt'
data = []
for line in open(filepath):
	data.append( [x for x in line.split() ] )

operat = data[0]

# processing c
c = data[2][2:]
c = list(map(int, c))
if operat == ['max']:
	c = list(map(lambda x: -x, c))
c = np.array(c)

#processing A
A = []
A_copy = []
for i in range(int(data[3][0])):
	if i == 0:
		A.append(data[4][2:])
	else:
		A.append(data[i+4])
for i in range(len(A)):
	A_copy.append(list(map(int, A[i])))
A = np.array(A_copy)

#processing b
b = data[i+5][2:]
b = np.array(list(map(int, b)))

#processing bounds
counts = data[i+6][2:]
bound = []
for i in range(int(data[1][0])):
	bound.append((int(counts[i]), None))

#minimizing
res = linprog(c, A_ub=A, b_ub=b, bounds=(tuple(bound)), callback=cb)
fun = res.fun * -1

print("Fun" + str(data[0]), fun, '\n')
x = res.x
#y = res.slack
for i in range(len(x)):
	print('x' + str(i) + ' ' + str(x[i]))
print('\n')
#for i in range(len(y)):
#	print('y'+str(i)+' '+str(y[i]))
