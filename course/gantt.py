import matplotlib.pyplot as plt
import sys
import numpy as np
import operator
import os
import matplotlib.patches as mpatches

def gantt_interval(list_of_oper):
	# функция для определения интервалов и построения диаграммы
	result = []
	# в переменных хранятся последние значения для ГВМ на абсциссе
	last_gvm = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
	last_op = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
			'8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0}
	for i in list_of_oper:
		for j in i:
			#в result записуеться [ГВМ, номер операции, x_start, x_end]
			if j[0] == 0:
				continue
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

def gantt_draw(filename):
	# Read data from file into variables
	y, c, x1, x2 = np.loadtxt(str(os.path.realpath(os.path.dirname(sys.argv[0]))) + '/datafile/' + filename + '.txt', unpack=True)
	# Map value to color
	colors = ['#f44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#212121',
		'#00BCD4', '#009688', '#4CAF50', '#8BC34A', '#FFEB3B', '#E65100', '#1B5E20',
		'#795548']
	color_mapper = np.vectorize(lambda x: {0: '#f44336', 1: '#E91E63', 2:'#9C27B0',
		3:'#673AB7', 4:'#3F51B5', 5:'#212121', 6:'#00BCD4', 7:'#009688',
		8:'#4CAF50', 9: '#8BC34A', 10: '#FFEB3B', 11: '#E65100', 12: '#1B5E20',
		13: '#795548', 14: '#607D8B'}.get(x))

	labels = ['detail1', 'detail2','detail3', 'detail4', 'detail5','detail6',
		'detail7', 'detail8', 'detail9', 'detail10',  'detail11',  'detail12',
		'detail13', 'detail14']

	# Plot a line for every line of data in your file
	plt.xlabel('Time')
	plt.ylabel('Equipment')
	plt.grid(linewidth=3)
	plt.title('Gantt chart ' + filename)
	plt.axis([0, max(x2) + 10, 0.5, 5.5])
	x = plt.hlines(y, x1, x2, colors=color_mapper(c), linewidths=75)
	patch = []
	for i in range(len(colors)):
		patch.append(mpatches.Patch(color=colors[i], label=labels[i]))
	plt.legend(handles=patch, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	labels = ['GVM1', 'GVM2', 'GVM3', 'GVM4', 'GVM5']
	plt.yticks([1, 2, 3, 4, 5], labels, rotation='vertical')
	#plt.legend(patch, labels)
	dir = os.path.dirname(sys.argv[0]) + '/img/'
	if not os.path.exists(dir):
		os.makedirs(dir)
	plt.savefig(str(os.path.realpath(os.path.dirname(sys.argv[0]))) + '/img/' + filename + '.png')
	wm = plt.get_current_fig_manager()
	wm.window.state('zoomed')
	plt.show()
	plt.clf()

def extend_gantt_draw(filename):
	# Read data from file into variables
	y, c, x1, x2 = np.loadtxt(str(os.path.realpath(os.path.dirname(sys.argv[0]))) + '/' + filename + '.txt', unpack=True)
	print('Час виробничого циклу = ', max(x2))
	# Map value to color
	colors = ['#f44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#212121',
		'#00BCD4', '#009688', '#4CAF50', '#8BC34A', '#FFEB3B', '#E65100', '#1B5E20',
		'#795548']
	color_mapper = np.vectorize(lambda x: {0: '#f44336', 1: '#E91E63', 2:'#9C27B0',
		3:'#673AB7', 4:'#3F51B5', 5:'#212121', 6:'#00BCD4', 7:'#009688',
		8:'#4CAF50', 9: '#8BC34A', 10: '#FFEB3B', 11: '#E65100', 12: '#1B5E20',
		13: '#795548', 14: '#607D8B'}.get(x))

	labels = ['detail1', 'detail2','detail3', 'detail4', 'detail5','detail6',
		'detail7', 'detail8', 'detail9', 'detail10',  'detail11',  'detail12',
		'detail13', 'detail14']

	# Plot a line for every line of data in your file
	plt.xlabel('Time')
	plt.ylabel('Equipment')
	plt.grid(linewidth=3)
	plt.title('Extented Gantt chart')
	plt.axis([0, max(x2) + 10, 0.5, 10.5])
	x = plt.hlines(y, x1, x2, colors=color_mapper(c), linewidths=35)
	patch = []
	for i in range(len(colors)):
		patch.append(mpatches.Patch(color=colors[i], label=labels[i]))
	plt.legend(handles=patch, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	labels = ['GVM1', 'GVM2', 'GVM3', 'GVM4', 'GVM5', 'ATM1', 'ATM2', 'ATM3', 'ATM4', 'ATM5']
	plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], labels, rotation='vertical')
	#plt.legend(patch, labels)
	dir = os.path.dirname(sys.argv[0]) + '/img/'
	if not os.path.exists(dir):
		os.makedirs(dir)
	plt.savefig(str(os.path.realpath(os.path.dirname(sys.argv[0]))) + '/img/' + filename + '.png')
	wm = plt.get_current_fig_manager()
	wm.window.state('zoomed')
	plt.show()
	plt.clf()

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
	TO = [list(map(float, i)) for i in TO]

	#
	y1 = []
	#
	y2 = []
    # для 4 преимества - правило минимальной остаточной трудоемкости
	y4 = []
	# для 5 преимества - правило макс операции
	y5 = []
	for j in range(M):
		# (ГВМ, общее вр. вып. на ГВМ, номер операции, вр. вып. на данном ГВМ)
		x1 = [(TM[i][0], sum(TO[i]), i, TO[i][0]) for i in range(N)]
		x1 = sorted(x1, key=operator.itemgetter(0, 1), reverse=True)
		x2 = [(TM[i][0], TO[i][0], i, TO[i][0]) for i in range(N)]
		x2 = sorted(x2, key=operator.itemgetter(0, 1))
		x4 = [(TM[i][0], sum(TO[i]), i, TO[i][0]) for i in range(N)]
		x4 = sorted(x4, key=operator.itemgetter(0, 1))
		x5 = [(TM[i][0], TO[i][0], i, TO[i][0]) for i in range(N)]
		x5 = sorted(x5, key=operator.itemgetter(0, 1), reverse=True)
		TO = [i[1:] for i in TO]
		TM = [i[1:] for i in TM]
		y1.append(x1)
		y2.append(x2)
		y4.append(x4)
		y5.append(x5)
	x1 = gantt_interval(y1)
	x2 = gantt_interval(y2)
	x4 = gantt_interval(y4)
	x5 = gantt_interval(y5)
	print('Правило максимальнои залишковои трудомисткости - ', x1[-1][3])
	print('Правило найкоротшои операции - ', round(x2[-1][3], 2))
	print('Правило минимальнои залишковои трудомисткости - ', round(x4[-1][3], 2))
	print('Правило найдовшои операции - ', x5[-1][3])
	# запись в файл для функции ganttDraw
	dir = os.path.dirname(sys.argv[0]) + '/datafile/'
	if not os.path.exists(dir):
		os.makedirs(dir)
	with open(str(os.path.realpath(os.path.dirname(sys.argv[0])))+'/datafile/'+'41.txt', 'w') as f:
		for i in x4:
			for j in i:
				f.write("%s " % j)
			f.write('\n')

	with open(str(os.path.realpath(os.path.dirname(sys.argv[0])))+'/datafile/'+'51.txt', 'w') as f:
		for i in x5:
			for j in i:
				f.write("%s " % j)
			f.write('\n')
	with open(str(os.path.realpath(os.path.dirname(sys.argv[0])))+'/datafile/'+'11.txt', 'w') as f:
		for i in x1:
			for j in i:
				f.write("%s " % j)
			f.write('\n')
	with open(str(os.path.realpath(os.path.dirname(sys.argv[0])))+'/datafile/'+'21.txt', 'w') as f:
		for i in x2:
			for j in i:
				f.write("%s " % j)
			f.write('\n')
	gantt_draw('11')
	gantt_draw('21')
	gantt_draw('41')
	gantt_draw('51')
	extend_gantt_draw('extendGantt')


if __name__=="__main__":
	main()
