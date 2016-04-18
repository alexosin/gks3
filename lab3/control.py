from gantt import gantt_criteria
from ganttDraw import gantt_draw
from itertools import permutations
from prettytable import PrettyTable
from johnson import johnson_order
from os import path
from sys import argv
import time
import progressbar

T = [[7, 3, 5],
	 [5, 6, 4],
	 [7, 5, 3],
	 [4, 6, 4]]
m = 3
n = 4
order = [0, 1, 2, 3]
#optimized_order = '1320'

filepath = str(path.realpath(path.dirname(argv[0]))) + '\data.txt'
data = []
for line in open(filepath):
	data.append( [x for x in line.split() ] )

m = int(data[0][2:][0])
n = int(data[1][2:][0])

T, T_copy = [], []
for i in data[2:]:
	T.append(i)

for i in range(len(T)):
	T_copy.append(list(map(int, T[i])))

T = T_copy[:]

johnson_order(T, m, n)
#optimized_order = input('Enter optimized order based on the table (first group time sorted by asc, second group time sorted by desc): ')
optimized_order = ['1320', '3120', '1302', '3102']
file_list = []
cmp_criter = []
perms = list(permutations(order, 4))
table = PrettyTable()
table.field_names = ['', 'crit11', 'crit22', 'crit25', 'crit27', 'crit33', 'crit35', 'crit36']
bar = progressbar.ProgressBar(max_value=len(perms) - 1)
print('\n')
for i in range(len(perms)):
	bar.update(i)
	time.sleep(0.1)
	criter, f = gantt_criteria(T, list(perms[i]))
	cmp_criter.append([f, criter])
	file_list.append(f)
	table.add_row([f, criter['crit11'], criter['crit22'], criter['crit25'], \
		criter['crit27'], criter['crit33'], criter['crit35'], criter['crit36']])
	gantt_draw(f)

print('\n', table)
maxim = {}
list_max = {}
maxim['crit11'] = min([i[1]['crit11'] for i in cmp_criter])
maxim['crit22'] = max([i[1]['crit22'] for i in cmp_criter])
maxim['crit25'] = min([i[1]['crit25'] for i in cmp_criter])
maxim['crit27'] = min([i[1]['crit27'] for i in cmp_criter])
maxim['crit33'] = min([i[1]['crit33'] for i in cmp_criter])
maxim['crit35'] = min([i[1]['crit35'] for i in cmp_criter])
maxim['crit36'] = min([i[1]['crit36'] for i in cmp_criter])

list_max['crit11'] = [i[0] for i in cmp_criter if i[1]['crit11']==maxim['crit11']]
list_max['crit22'] = [i[0] for i in cmp_criter if i[1]['crit22']==maxim['crit22']]
list_max['crit25'] = [i[0] for i in cmp_criter if i[1]['crit25']==maxim['crit25']]
list_max['crit27'] = [i[0] for i in cmp_criter if i[1]['crit27']==maxim['crit27']]
list_max['crit33'] = [i[0] for i in cmp_criter if i[1]['crit33']==maxim['crit33']]
list_max['crit35'] = [i[0] for i in cmp_criter if i[1]['crit35']==maxim['crit35']]
list_max['crit36'] = [i[0] for i in cmp_criter if i[1]['crit36']==maxim['crit36']]

johnson_cmp = {}
for i in optimized_order:
	johnson_cmp[i] = {}

for u in optimized_order:
	for i in cmp_criter:
		if i[0] == u:
			if i[1]['crit11'] == maxim['crit11']:
				johnson_cmp[u]['crit11']  = 'Yes'
			else:
				johnson_cmp[u]['crit11'] = 'No'
			if i[1]['crit22'] == maxim['crit22']:
				johnson_cmp[u]['crit22']  = 'Yes'
			else:
				johnson_cmp[u]['crit22'] = 'No'
			if i[1]['crit25'] == maxim['crit25']:
				johnson_cmp[u]['crit25']  = 'Yes'
			else:
				johnson_cmp[u]['crit25'] = 'No'
			if i[1]['crit27'] == maxim['crit27']:
				johnson_cmp[u]['crit27']  = 'Yes'
			else:
				johnson_cmp[u]['crit27'] = 'No'
			if i[1]['crit33'] == maxim['crit33']:
				johnson_cmp[u]['crit33']  = 'Yes'
			else:
				johnson_cmp[u]['crit33'] = 'No'
			if i[1]['crit35'] == maxim['crit35']:
				johnson_cmp[u]['crit35']  = 'Yes'
			else:
				johnson_cmp[u]['crit35'] = 'No'
			if i[1]['crit36'] == maxim['crit36']:
				johnson_cmp[u]['crit36']  = 'Yes'
			else:
				johnson_cmp[u]['crit36'] = 'No'

table2 = PrettyTable()
table2.field_names = ['','value',  'optimized', '3102', '1302', '3120', '1320']
for i in list_max:
	table2.add_row([i, maxim[i], list_max[i], johnson_cmp['3102'][i],
				johnson_cmp['1302'][i], johnson_cmp['3120'][i],
				johnson_cmp['1320'][i]])
print(table2)
