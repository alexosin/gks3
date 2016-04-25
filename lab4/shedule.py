import operator
import os
import sys

sys.path.append(sys.argv[0][:-16])
from lab3 import ganttDraw

def gantt_interval(list_of_oper):
	# функция для определения интервалов и построения диаграммы
	result = []
	# в переменных хранятся последние значения для ГВМ на абсциссе
	last_gvm = {'1': 0, '2': 0, '3': 0}
	last_op = {'0': 0, '1': 0, '2': 0, '3': 0}
	for i in list_of_oper:
		for j in i:
			#в result записуеться [ГВМ, номер операции, x_start, x_end]
			result.append([j[0], j[2],
				max(last_gvm[str(j[0])], last_op[str(j[2])]),
				max(last_gvm[str(j[0])], last_op[str(j[2])]) + j[3]])
			last_gvm[str(j[0])] = max(last_gvm[str(j[0])], last_op[str(j[2])]) + j[3]
			last_op[str(j[2])]  = last_gvm[str(j[0])]
	return result

def ordered_timetable(timetable):
	# функция для сортировки и записи интервалов по ГВМ
	ort = []
	for i in range(1, 4):
		x = [k[2:] for k in timetable if k[0] == i]
		ort.append(x)
	return ort

def downtime(timetable):
	tkp = [] # суммарное время простоя единицы оборудования
	for i in timetable: # nk - количество простоев
		sums = 0
		for j in range(len(i)-1):
			x = i[j + 1][0] - i[j][1]
			sums += x
		sums += i[0][0]
		tkp.append(sums)
	return min(tkp)

def main():
	filepath = str(os.path.realpath(os.path.dirname(sys.argv[0]))) + '\data.txt'
	data = []
	for line in open(filepath):
		data.append([x for x in line.split()])

	M = int(data[0][2])
	N = int(data[1][2])
	TM = []
	TO = []
	for i in range(N):
		if i == 0:
			TM.append(data[2][2:])
		else:
			TM.append(data[i+2])

	for i in range(N):
		if i == 0:
			TO.append(data[2+N][2:])
		else:
			TO.append(data[2+N+i])

	TM = [list(map(int, i)) for i in TM]
	TO = [list(map(int, i)) for i in TO]

    # для 4 преимества - правило минимальной остаточной трудоемкости
	y4 = []
	# для 5 преимества - правило макс операции
	y5 = []
	for j in range(M):
		# (ГВМ, общее вр. вып. на ГВМ, номер операции, вр. вып. на данном ГВМ)
		x4 = [(TM[i][0], sum(TO[i]), i, TO[i][0]) for i in range(4)]
		x4 = sorted(x4, key=operator.itemgetter(0, 1))
		x5 = [(TM[i][0], TO[i][0], i, TO[i][0]) for i in range(4)]
		x5 = sorted(x5, key=operator.itemgetter(0, 1), reverse=True)
		TO = [i[1:] for i in TO]
		TM = [i[1:] for i in TM]
		y4.append(x4)
		y5.append(x5)

	x4 = gantt_interval(y4)
	x5 = gantt_interval(y5)

	with open(str(os.path.realpath(os.path.dirname(sys.argv[0])))+'/datafile/'+'41.txt', 'w') as f:
		f.write('0.5 4 0 30\n')
		for i in x4:
			for j in i:
				f.write("%s " % j)
			f.write('\n')
		f.write('3.5 4 0 0')

	with open(str(os.path.realpath(os.path.dirname(sys.argv[0])))+'/datafile/'+'51.txt', 'w') as f:
		f.write('0.5 4 0 30\n')
		for i in x5:
			for j in i:
				f.write("%s " % j)
			f.write('\n')
		f.write('3.5 4 0 0')
	ganttDraw.gantt_draw('41')
	ganttDraw.gantt_draw('51')

	# для подсчета простоев сорт. наше расписание по ГВМ
	x4 = ordered_timetable(x4)
	x5 = ordered_timetable(x5)
	print("Простоi:")
	print("  Для четвертого правила - %s" % downtime(x4))
	print("  Для п'ятого правила - %s" % downtime(x5))
if __name__ == "__main__":
	main()
