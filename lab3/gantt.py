from os import path
from sys import argv
from random import choice
import copy
from ganttDraw import gantt_draw

def gantt_criteria(T, order):
	def get_column(matrix, col):
		# get column - matrix[col]
		return [i[col] for i in matrix]

	def get_sorted_matrix(matrix, order):
		# sorted our matrix by order
		return_matrix = []
		for i in order:
			return_matrix.append(matrix[i])
		return return_matrix

	def timetable(column, lasters, ii):
		# calculate time between operations
		x = []
		if ii == 0:
			for i in range(len(column)):
				lasters['1'][i + 1] = lasters['1'][i] + column[i]
				lasters['2'][i] = lasters['1'][i] + column[i]
				y = [lasters['1'][i], lasters['1'][i]+column[i]]
				x.append(y)
				#print(i, y)
			lasters['1'] = [i[1] for i in x]
			lasters['1'].append(0)
		if ii == 1:
			for i in range(len(column)):
				lasters['2'][i + 1] = lasters['2'][i] + column[i]
				lasters['3'][i] = lasters['2'][i] + column[i]
				if (lasters['2'][i + 1] < lasters['1'][i+1]):
					lasters['2'][i + 1] = lasters['1'][i+1]
				y = [lasters['2'][i], lasters['2'][i]+column[i]]
				x.append(y)
				#print(i, y)
			lasters['2'] = [i[1] for i in x]
			lasters['2'].append(0)
		if ii == 2:
			for i in range(len(column)):
				lasters['3'][i + 1] = lasters['3'][i] + column[i]
				if (lasters['3'][i + 1] < lasters['2'][i+1]):
					lasters['3'][i + 1] = lasters['2'][i+1]
				y = [lasters['3'][i], lasters['3'][i]+column[i]]
				x.append(y)
			lasters['3'] = [i[1] for i in x]
			lasters['3'].append(0)
		return lasters, x

	TT = get_sorted_matrix(T, order)
	lasters = {'1': [0, 0, 0, 0, 0], '2': [0, 0, 0, 0, 0], '3': [0, 0, 0, 0, 0]}
	timetable_matrix = []
	buff = []
	for i in range(3):
			col = get_column(TT, i)
			lasters, buff = timetable(col, lasters, i)
			timetable_matrix.append(buff)

	trash_matrix = copy.deepcopy(timetable_matrix)

	for i in range(len(timetable_matrix)):
		for j in timetable_matrix[i]:
			j.insert(0, i + ( (i+1) * 5) - i)

	for i in range(len(timetable_matrix)):
		u = 0
		for j in timetable_matrix[i]:
			j.insert(1, order[u])
			u += 1

	s = ''
	for i in order:
		s += str(i)
	filename = s
	f = open(str(path.realpath(path.dirname(argv[0]))) + '/datafile/' + filename + '.txt', 'w')
	f.write('0 4 0 35\n')
	for i in range(len(timetable_matrix)):
		for j in timetable_matrix[i]:
			for u in j:
				f.write("%s " % u)
			f.write('\n')
	f.write('20 4 0 0')
	f.close()

	def criterion(matrix, input_matrix, trash):
		# calculate for 7 criterion

		#criterion1
		criter = {}
		for i in matrix:
			x = list(map(lambda y: max(y), [j[2:] for j in i]))
		criter['crit11'] = max(x)
		# criterion2
		x, y = [], []
		for i in range(3):
			x.append(sum(get_column(input_matrix, i)))
		for i in trash:
			sums = 0
			for j in range(len(i)-1):
				sums += i[j + 1][0] - i[j][1]
			y.append(sums)
		y = list(map(lambda x: x+1, y))
		u = list(map(lambda l1, l2: l1 + l2, x, y))
		x = sum(map(lambda l1, l2: l1/l2, x, u))
		criter['crit22'] = x
		#criterion3
		criter['crit25'] = sum(y)
		#criterion4
		k = list(map(lambda y: y/4, y))
		criter['crit27'] = sum(k)
		#criterion5
		k, y, u = [], [], []
		for i in range(len(trash)):
			k.append(get_column(trash, i))
		for i in k:
			sums = 0
			x = []
			for j in range(len(i)-1):
				if j == 0:
					sums += i[j][0]
				sums += i[j + 1][0] - i[j][1]
				x.append(i[j + 1][0] - i[j][1])
			y.append(sums)
		criter['crit33'] = sum(y)
		#criterion6
		x = []
		for i in y:
			if i:
				x.append(sum(y) / i)

		criter['crit35'] = max(x)
		#criterion7
		k = list(map(lambda y: y/4, y))
		criter['crit36'] = sum(k)

		return criter

	criter = criterion(timetable_matrix, T, trash_matrix)
	return criter, filename

if __name__ == '__main__':
	T = [[7, 3, 5],
		 [5, 6, 4],
		 [7, 5, 3],
		 [4, 6, 4]]
	order = [2, 0, 1, 3]
	o = [0, 2, 1,3]
	c, f = gantt_criteria(T, order)
	gantt_draw(f)
	c, f = gantt_criteria(T, o)
	gantt_draw(f)
