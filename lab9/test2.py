# программа для подсчета среднеквадратического, максимального отколонении
# и суммы отклонений для трех методов интерполяции: с прогнозированием
# с постоянной частотой и ЦДА

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import numpy as np
import circle

def plot_fault(f0, f1, f2, f3, name):
	# функция для построения графиков для f1 - ошибка интерполяции с прогнозированием
	# f2 - на постоянной несучей частоте; f3 - ЦДА
	plt.plot(f0, f1,  '-', label='predict', color='r')
	plt.plot(f0, f2, '-', label='const freq', color='g')
	plt.plot(f0, f3, '-', label='corrections_forecast', color='b')
	plt.grid()
	plt.title(name)
	plt.legend(loc='best')
	plt.show()

def step_fault():
	print('\nFault step')
	fault1, fault2, fault3 = [], [], []
	for j in range(1, 10):
		circle1 = circle.CirclePath((70, 85), 30, T=3, V= 5, step=j)
		circle1.get_path_by_interpolation_predict()
		circle1.method_cont_carrier_freq()
		circle1.corrections_forecast()
		def find_fault(data):
			faults = []
			points = list(zip(data['x'], data['y']))
			for i in points:
				faults.append(abs(circle1.radius - circle1.get_distance_between_center_and_point(i[0], i[1])))
			return(j, np.mean(faults), max(faults), sum(faults))
		fault1.append(find_fault(circle1.inter_predict))
		fault2.append(find_fault(circle1.inter_freq))
		fault3.append(find_fault(circle1.cor_for))
	for j in range(1,4):
		zero = [i[0] for  i in fault1]
		first =  [i[j] for i in fault1]
		second = [i[j] for i in fault2]
		third =  [i[j] for i in fault3]
		table1 = PrettyTable()
		table1.field_names = ['step', 'predict', 'const freq', 'corrections_forecast']
		for i in range(len(fault1)):
			table1.add_row([zero[i], first[i], second[i], third[i]])
		print(table1)
		plot_fault(zero, first, second, third, 'Step')

def radius_fault():
	print('\nAngle fault')
	fault1, fault2, fault3 = [], [], []
	for j in range(20, 70, 5):
		circle1 = circle.CirclePath((70, 85), j, T=3, V= 5, step=5)
		circle1.get_path_by_interpolation_predict()
		circle1.method_cont_carrier_freq()
		circle1.corrections_forecast()
		def find_fault(data):
			faults = []
			points = list(zip(data['x'], data['y']))
			for i in points:
				faults.append(abs(circle1.radius - circle1.get_distance_between_center_and_point(i[0], i[1])))
			return(j, np.mean(faults), max(faults), sum(faults))
		fault1.append(find_fault(circle1.inter_predict))
		fault2.append(find_fault(circle1.inter_freq))
		fault3.append(find_fault(circle1.cor_for))
	for j in range(1,4):
		zero = [i[0] for  i in fault1]
		first =  [i[j] for i in fault1]
		second = [i[j] for i in fault2]
		third =  [i[j] for i in fault3]
		table1 = PrettyTable()
		table1.field_names = ['step', 'predict', 'const freq', 'corrections_forecast']
		for i in range(len(fault1)):
			table1.add_row([zero[i], first[i], second[i], third[i]])
		print(table1)
		plot_fault(zero, first, second, third, 'Radius')

def freq_fault():
	fault2, fault3 = [], []
	for j in range(2, 10):
		circle1 = circle.CirclePath((70, 85), 30, T=j, V= 5, step=5)
		circle1.get_path_by_interpolation_predict()
		circle1.method_cont_carrier_freq()
		circle1.corrections_forecast()
		def find_fault(data):
			faults = []
			points = list(zip(data['x'], data['y']))
			for i in points:
				faults.append(abs(circle1.radius - circle1.get_distance_between_center_and_point(i[0], i[1])))
			return(j, np.mean(faults), max(faults), sum(faults))
		fault2.append(find_fault(circle1.inter_freq))
		fault3.append(find_fault(circle1.cor_for))
	for j in range(1,4):
		zero = [i[0] for  i in fault2][:-2]
		second = [i[j] for i in fault2][:-2]
		third =  [i[j] for i in fault3][:-2]
		table1 = PrettyTable()
		table1.field_names = ['T', 'const freq', 'corrections_forecast']
		for i in range(len(zero)):
			table1.add_row([zero[i], second[i], third[i]])
		print(table1)
		plot_fault(zero, [0 for i in range(len(zero))], second, third, 'T')

def main():
	step_fault()
	radius_fault()
	freq_fault()

if __name__=="__main__":
	main()
