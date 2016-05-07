import operator
import os
import sys
import numpy
import natsort
from colorama import Style, Fore
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
	tkp, kp = [], [] # суммарное время простоя единицы оборудования
	end_work = max(max([max(i) for i in timetable]))
	for i in timetable: # nk - количество простоев
		sums = []
		for j in range(len(i)-1):
			x = i[j + 1][0] - i[j][1]
			sums.append(x)
		sums.insert(j+1, end_work-i[j+1][1])
		tkp.append(sums)
	return tkp

def waiting(x):
	tijo = [] # tij0 - ожидание детали на операцию, nj - кол. ожид.
	#x = [get_column(trash, i) for i in range(4)]
	for i in x:
		sums = []
		for j in range(len(i)-1):
			x = i[j + 1][0] - i[j][1]
			sums.append(x)
		sums.insert(0, i[0][0])
		tijo.append(sums)
	return tijo

def control_timetable(timetable, header):
	print(Fore.YELLOW + '{:-^30}'.format(header))
	start_order_details = []
	for i in range(1, 4):
		start_order_details.append([j[1] for j in timetable if j[0] == i])

	# разбиваем интервалы по деталям, выйдет 4 списка, использ.
	# для подсчета ожидания
	order_by_details = []
	for i in start_order_details[0]:
		order_by_details.append([j for j in timetable if j[1] == i])

	# для подсчета простоев сорт. наше расписание по ГВМ
	timetable = ordered_timetable(timetable)

	# список порядка запуска деталей на ГВМ, убираем номер операции
	# и ГВМ со списка интервалов, для обсчета ожидания
	start_order_gvm = []
	order_by_details_norm = []
	for i in order_by_details:
		start_order_gvm.append([j[:1][0] for j in i])
		order_by_details_norm.append([j[2:] for j in i])

	# считаем послеоперационные простои ГВМ
	timetable = downtime(timetable)
	for i in range(3):
		index = natsort.index_natsorted(start_order_details[i])
		timetable[i] = natsort.order_by_index(timetable[i], index)

	print(Fore.WHITE + "\nDowntime: " + Fore.CYAN +
		'{}'.format(min([sum(i) for i in timetable])))
	for i in timetable:
		print(Fore.WHITE + '{!s:>18s}'.format(i))

	# считаем ожидание деталей перед обработкой
	print("\nWaiting:")
	order_by_details = waiting(order_by_details_norm)
	# упорядочиваем ожидание для каждой детали по ГВМ: 1 2 3
	index = natsort.index_natsorted(start_order_details[0])
	order_by_details = natsort.order_by_index(order_by_details, index)
	start_order_gvm = natsort.order_by_index(start_order_gvm, index)
	for i in range(4):
		index = natsort.index_natsorted(start_order_gvm[i])
		order_by_details[i] = natsort.order_by_index(order_by_details[i],
											index)

	for i in order_by_details:
		print(Fore.WHITE + '{!s:>16s}'.format(i))

	#считаем локальний резерв
	order_by_details = numpy.transpose(order_by_details)
	print('\nLocal resource:\n')
	for i in range(3):
		for j in range(4):
			first = timetable[i][j]
			try:
				second = order_by_details[i+1][j]
			except IndexError:
				second = float('inf')
			print("      L({0}, {1}) = min({2}, {3}) = {4}".format( \
				i+1, j+1, first, second, min(first, second)))
		print('\n')
	print(Style.RESET_ALL)

def main():
	filepath = str(os.path.realpath(os.path.dirname(sys.argv[0]))) + '\data.txt'
	data = []
	for line in open(filepath):
		data.append([x for x in line.split()])
	# ввод данных с файла
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
	# запись в файл для функции ganttDraw
	dir = os.path.dirname(sys.argv[0]) + '/datafile/'
	if not os.path.exists(dir):
		os.makedirs(dir)
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
	control_timetable(x4, '4 rule')
	control_timetable(x5, '5 rule')

if __name__ == "__main__":
	main()
