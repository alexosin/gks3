# программа для подсчета среднеквадратического, максимального отколонении
# и суммы отклонений для трех методов интерполяции: с прогнозированием
# с постоянной частотой и ЦДА

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import numpy as np
import line

def plot_fault(f0, f1, f2, f3, name):
	# функция для построения графиков для f1 - ошибка интерполяции с прогнозированием
	# f2 - на постоянной несучей частоте; f3 - ЦДА
	plt.plot(f0, f1,  '-', label='predict', color='r')
	plt.plot(f0, f2, '-', label='const freq', color='g')
	plt.plot(f0, f3, '-', label='cda', color='b')
	plt.grid()
	plt.title(name)
	plt.legend(loc='best')
	plt.show()

def step_fault(line):
	print('\nFault step')
	fault1, fault2, fault3 = [], [], []
	for j in range(1, 10):
		line.calc_parametr(T=3, V=5, step=j)
		line.get_path_by_interpolation_predict(j)
		line.method_cont_carrier_freq()
		line.CDA()
		def find_fault(data):
			faults = []
			points = list(zip(data['x'], data['y']))
			for i in points:
				faults.append(line.find_distance(i))
			#print(j, np.mean(faults), max(faults), sum(faults))
			return(j, np.mean(faults), max(faults), sum(faults))
		fault1.append(find_fault(line.inter_predict))
		fault2.append(find_fault(line.inter_freq))
		fault3.append(find_fault(line.inter_cda))
	for j in range(1,4):
		zero = [i[0] for  i in fault1]
		first =  [i[j] for i in fault1]
		second = [i[j] for i in fault2]
		third =  [i[j] for i in fault3]
		table1 = PrettyTable()
		table1.field_names = ['step', 'predict', 'const freq', 'cda']
		for i in range(len(fault1)):
			table1.add_row([zero[i], first[i], second[i], third[i]])
		print(table1)
		plot_fault(zero, first, second, third, 'Step')

def angle_fault():
	print('\nAngle fault')
	fault1, fault2, fault3 = [], [], []
	for j in range(1, 90):
		line1 = line.LinePath((20, 25), (40, 85), j)
		line1.get_endpoint_by_angle()
		line1.get_line_func()
		line1.calc_parametr(T=3, V=5, step=5)
		line1.get_path_by_interpolation_predict(5)
		line1.method_cont_carrier_freq()
		line1.CDA()
		def find_fault(data):
			faults = []
			points = list(zip(data['x'], data['y']))
			for i in points:
				faults.append(line1.find_distance(i))
			return(j, np.mean(faults), max(faults), sum(faults))
		fault1.append(find_fault(line1.inter_predict))
		fault2.append(find_fault(line1.inter_freq))
		fault3.append(find_fault(line1.inter_cda))
	for j in range(1,4):
		zero = [i[0] for  i in fault1]
		first =  [i[j] for i in fault1]
		second = [i[j] for i in fault2]
		third =  [i[j] for i in fault3]
		table1 = PrettyTable()
		table1.field_names = ['angle', 'predict', 'const freq', 'cda']
		for i in range(len(fault1)):
			table1.add_row([zero[i], first[i], second[i], third[i]])
		print(table1)
		plot_fault(zero, first, second, third, 'Angle')

def freq_fault(line):
	fault2, fault3 = [], []
	for j in range(1, 9):
		line.calc_parametr(T=j, V=5, step=5)
		line.method_cont_carrier_freq()
		line.CDA()
		def find_fault(data):
			faults = []
			points = list(zip(data['x'], data['y']))
			for i in points:
				faults.append(line.find_distance(i))
			return(j, np.mean(faults), max(faults), sum(faults))
		fault2.append(find_fault(line.inter_freq))
		fault3.append(find_fault(line.inter_cda))
	for j in range(1,4):
		zero = [i[0] for  i in fault2][:-2]
		second = [i[j] for i in fault2][:-2]
		third =  [i[j] for i in fault3][:-2]
		table1 = PrettyTable()
		table1.field_names = ['T', 'const freq', 'cda']
		for i in range(len(zero)):
			table1.add_row([zero[i], second[i], third[i]])
		print(table1)
		plot_fault(zero, [0 for i in range(len(zero))], second, third, 'T')

def main():
	start, end = [(20, 25), (40, 85)]
	angle = 71
	line1 = line.LinePath(start, end, angle)
	line1.get_endpoint_by_angle()
	line1.get_line_func()
	step_fault(line1)
	angle_fault()
	freq_fault(line1)

if __name__=="__main__":
	main()
