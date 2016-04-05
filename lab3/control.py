from gantt import gantt_criteria
from ganttDraw import gantt_draw
from itertools import permutations
from prettytable import PrettyTable
from johnson import johnson_order
from os import path
from sys import argv

T = [[7, 3, 5],
	 [5, 6, 4],
	 [7, 5, 3],
	 [4, 6, 4]]
m = 3
n = 4
order = [0, 1, 2, 3]

filepath = str(path.realpath(path.dirname(argv[0]))) + '\data.txt'
data = []
for line in open(filepath):
	data.append( [x for x in line.split() ] )

print(data)
m = int(data[0][2:][0])
n = int(data[1][2:][0])

T, T_copy = [], []
for i in data[2:]:
	T.append(i)

for i in range(len(T)):
	T_copy.append(list(map(int, T[i])))

T = T_copy[:]

johnson_order(T, m, n)

file_list = []
perms = list(permutations(order, 4))
table = PrettyTable()
table.field_names = ['', 'crit11', 'crit22', 'crit25', 'crit27', 'crit33', 'crit35', 'crit36']
for i in perms:
	criter, f = gantt_criteria(T, list(i))
	file_list.append(f)
	table.add_row([f, criter['crit11'], criter['crit22'], criter['crit25'], \
		criter['crit27'], criter['crit33'], criter['crit35'], criter['crit36']])

def draw(fl):
	for i in fl:
		gantt_draw(i)

draw(file_list)
print(table)
