from prettytable import PrettyTable
import itertools

def johnson_order(T, m, n):
	def cmp(x):
		# choose logic operations
		if x[0] > x[1]:
			return '>'
		elif x[0] < x[1]:
			return '<'
		else:
			return '='

	def ins(list1, list2, index):
		# insert list2 elements to list1[index]
		for j in list1:
			j.insert(index, list2[list1.index(j)])

	def divided(list):
		group = {'t1':[], 't2':[]}
		for i in list:
			if i[2] == '<':
				group['t1'].append(int(i[0][2:]) - 1)
			else:
				group['t2'].append(int(i[0][2:]) - 1)
		return group

	M = [[i[0] + i[1], i[2] + i[1]] for i in T]
	oper = list(map(cmp, M))
	ins(M, oper, 1)
	to = ['TO'+str(i+1) for i in range(m)]
	to.insert(0, '')
	td = ['TD'+str(i+1) for i in range(n)]
	ins(M, td, 0)
	table = PrettyTable()
	table.field_names = [i for i in to]
	for i in range(n):
		table.add_row([j for j in M[i]])
	print(table)

	groups = divided(M)

	for i in groups:
		print(str(i[1:]) + ': ' + str(groups[i]))

if __name__ == "__main__":
	T = [[7, 3, 5],
		 [5, 6, 4],
		 [7, 5, 3],
		 [4, 6, 4]]
	m = 3
	n = 4
	johnson_order(T, m, n)
