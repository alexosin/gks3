from gantt import gantt_criteria
from ganttDraw import gantt_draw
from itertools import permutations
from prettytable import PrettyTable

T = [[7, 3, 5],
	 [5, 6, 4],
	 [7, 5, 3],
	 [4, 6, 4]]

order = [0, 1, 2, 3]

perms = list(permutations(order, 4))

table = PrettyTable()
table.field_names = ['', 'crit11', 'crit22', 'crit25', 'crit27', 'crit33', 'crit35', 'crit36']
for i in perms:
	criter, filename = gantt_criteria(T, list(i))
	table.add_row([filename, criter['crit11'], criter['crit22'], criter['crit25'], \
				criter['crit27'], criter['crit33'], criter['crit35'], criter['crit36']])
	gantt_draw(filename)

print(table)
