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
			j.insert(0, i + ((i+1) * 5) - i)

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

	def criterion(input_matrix, trash):
		# calculate for 7 criterion
		criter = {}
		for i in trash: # tijk - момент окончания выполнения операции Lij
			tijk = list(map(lambda y: max(y), [j for j in i]))
		tkr, tkp, nk = [], [], [] # tkr - суммарное время выпол. операции на единице обор.
		for i in range(3): # tkp - суммарное время простоя единицы обор.
			tkr.append(sum(get_column(input_matrix, i)))
		for i in trash: # nk - количество простоев
			sums, pros = 0, 0
			for j in range(len(i)-1):
				x = i[j + 1][0] - i[j][1]
				sums += x
				if x:
					pros += 1
			sums += i[0][0]
			if i[0][0]:
				pros += 1
			tkp.append(sums)
			nk.append(pros)
		tijo, nj = [], [] # tij0 - ожидание детали на операцию, nj - кол. ожид.
		x = [get_column(trash, i) for i in range(4)]
		for i in x:
			sums, pros = 0, 0
			for j in range(len(i)-1):
				x = i[j + 1][0] - i[j][1]
				sums += x
				if x:
					pros += 1
			sums += i[0][0]
			if i[0][0]:
				pros += 1
			tijo.append(sums)
			nj.append(pros)
		criter = {}
		criter['crit11'] = max(tijk)
		criter['crit22'] = round(sum(map(lambda l1, l2: l1/(l1 + l2),
															tkr, tkp)), 2)
		criter['crit25'] = sum(tkp)
		criter['crit27'] = round(sum(map(lambda l1, l2: l1/l2 if l2 != 0 else 0,
															tkp, nk)), 2)
		criter['crit33'] = sum(tijo)
		criter['crit35'] = max(map(lambda l1, l2: l1/l2 if l2 != 0 else 0,
															tijo, nj))
		criter['crit36'] = round(sum(map(lambda l1, l2: l1/l2 if l2 != 0 else 0,
															tijo, nj)), 1)
		return criter
	criter = criterion(T, trash_matrix)
	return criter, filename

if __name__ == '__main__':
	T = [[7, 3, 5],
		 [5, 6, 4],
		 [7, 5, 3],
		 [4, 6, 4]]
	order = [1, 0, 3, 2]
	#o = [0, 2, 1,3]
	c, f = gantt_criteria(T, order)
	gantt_draw(f)
	#c, f = gantt_criteria(T, o)
	#gantt_draw(f)
