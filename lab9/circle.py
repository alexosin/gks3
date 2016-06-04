import matplotlib.pyplot as plt
import math
import sys
sys.path.append(sys.argv[0][:-14])
from lab8 import line

class CirclePath:
	def __init__(self, center, radius, T, V, step, angle_degrees=(0, 90)):
		# center - (centerX, centerY)
		# angle_degrees - (start, end) work only with (0, 90)
		self.centerX = center[0]
		self.centerY = center[1]
		self.radius = radius
		self.angle_degrees = angle_degrees
		self.T = T
		self.V = V
		self.step = step
		self.start = (self.centerX+radius, self.centerY)
		self.end = (self.centerX, self.centerY + self.radius)
		self.calc_parameter()

	def calc_parameter(self):
		# считаем координаты для построения окружности

		# используем радианы
		# если начинаем с нулевого градуса, тогда его сразу записываем в
		# список радианов
		list_radians = [] if self.angle_degrees[0] else [0]
		start_angle = self.angle_degrees[0] + 1 if list_radians \
				else self.angle_degrees[0]

		for i in range(start_angle, self.angle_degrees[1]):
		    float_div = 180.0/(i)
		    list_radians.append(math.pi/float_div)

		self.list_x2_axis = []
		self.list_y2_axis = []

		for a in list_radians:
		    self.list_x2_axis.append(self.radius * math.cos(a) + self.centerX)
		    self.list_y2_axis.append(self.radius * math.sin(a) + self.centerY)

		angle = (self.angle_degrees[0] + self.angle_degrees[1]) / 2
		self.bisector = line.LinePath(start=(self.centerX, self.centerY),
				angle=angle, length=self.radius+5)
		# найдем координаты бисектрисы
		self.bisector.get_endpoint_by_angle()
		self.bisector.get_line_func()

		# считаем значение тау, дельта-фи, количества итераций
		self.tau = (math.pi*self.radius) / (2 * self.V)
		self.R = math.sqrt(self.start[0]**2 + self.start[1]**2)
		self.deltaFi = (self.V * self.T) / self.R
		self.imax = math.floor(self.tau / self.T)

	def get_distance_between_center_and_point(self, pointX, pointY):
		# найти расстояние между жвумя точками
		return math.sqrt((pointX-self.centerX)**2 + (pointY-self.centerY)**2)

	def get_path_by_interpolation_predict(self, plotted=False):
		# метод для построения траектории с помощью линейной интерполяции
		# оценночной функции с прогнозированием шага
		x_points, y_points = [], []
		x_points.append(self.start[0])
		y_points.append(self.start[1])
		x = self.start[0] - self.step
		y = self.start[1] + self.step
		x_points.append(x)
		y_points.append(y)
		while x >= (y - self.bisector.b) / self.bisector.k:
			if self.get_distance_between_center_and_point(x, y) >= self.radius:
				x = x - self.step
				y = y + self.step
			else:
				y = y + self.step
			x_points.append(x)
			y_points.append(y)
		while x >= self.end[0]:
			if self.get_distance_between_center_and_point(x, y) >= self.radius:
				x = x - self.step
			else:
				x = x - self.step
				y = y + self.step
			x_points.append(x)
			y_points.append(y)
		self.inter_predict = {'x2': x_points, 'y2': y_points}
		x_points = [i + self.step for i in x_points[1:]]
		y_points = [i - self.step for i in y_points[1:]]
		x_points.append(self.end[0])
		y_points.append(self.end[1])
		self.inter_predict['x'] = x_points
		self.inter_predict['y'] = y_points
		if plotted:
			self.plot_inter1()

	def method_cont_carrier_freq(self, plotted = False):
		# метод оценочной функции на постоянной несущей частоте
		x_points, y_points = [], []
		x_growth, y_growth = [], []

		x_end = self.start[0]
		y_end = self.start[1]

		last_delta_x = 0
		last_delta_y = 0
		if plotted:
			print('\nFrequence Interpolation')
		for i in range(1, self.imax+1):
			delta_x = 0
			delta_y = 0
			x = x_end * i
			y = y_end * i
			while True:
				N = last_delta_x - self.deltaFi * y
				M = last_delta_y - self.deltaFi * x
				if N >= 0 and M >= 0:
					break
				if N < 0:
					delta_x = delta_x + self.step
					last_delta_x = delta_x
					x = x_end - delta_x
				if M < 0:
					delta_y = delta_y + self.step
					last_delta_y = delta_y
					y = y_end - delta_y
				if plotted:
					print('N = {}, delta_x = {}, x = {}, M = {}, delta_y = {}, y = {}'
							.format(N, x, delta_x, M, delta_y, y))
			print("{0}: delta_x{0} = {1}, delta{0} = {2}".format(i, delta_x, delta_y))
			x_growth.append(delta_x)
			y_growth.append(delta_y)
			x_end = x
			y_end = y
		# находим точки для построения траектории
		x_points.append(self.start[0])
		y_points.append(self.start[1])
		for i in range(len(x_growth)):
			x_points.append(x_points[-1] - x_growth[i])
			y_points.append(y_points[-1] + y_growth[i])
		self.inter_freq = {'x': x_points, 'y': y_points}
		if plotted:
			self.plot_inter2()

	def corrections_forecast(self, plotted=False):
		x_end = self.start[0]
		y_end = self.start[1]
		x_points, y_points = [x_end], [y_end]
		print(self.deltaFi)
		if plotted:
			print("\nMethod of corrections and forecast")
		while True:
			full_x = y_end * self.deltaFi
			full_y = x_end * self.deltaFi
			dx = int(full_x / self.step) * self.step
			dy = int(full_y / self.step) * self.step
			x_end -= dx
			y_end += dy
			if plotted:
				print("fx = {}, delta_x = {}, x = {}, fy = {}, delta_y = {}, y = {}"
						.format(full_x, dx, x_end, full_y, 	dy, y_end))
			if  x_end < self.end[0] or y_end >= self.end[1]:
				break
			x_points.append(x_end)
			y_points.append(y_end)
			if self.get_distance_between_center_and_point(x_end, y_end) >= self.radius:
				x_end += self.step
				y_end -= self.step
		if x_points[-1] > self.end[0]:
			x_points.append(self.end[0])
			y_points.append(self.end[1])
		self.cor_for = {'x': x_points, 'y': y_points}
		if plotted:
			self.plot_inter3()

	def plot_inter1(self):
		# интерполяция за методом прогнозирования шага
		plt.axis('equal')
		plt.plot([self.bisector.start[0], self.bisector.endx],
				[self.bisector.start[1], self.bisector.endy], '--')
		plt.plot(self.list_x2_axis,self.list_y2_axis,c='b')
		plt.plot(self.inter_predict['x'], self.inter_predict['y'], '-', color='k')
		plt.plot(self.inter_predict['x2'], self.inter_predict['y2'], '--', color='r')
		plt.title('Interpolation 1')
		plt.grid(True)
		plt.show()

	def plot_inter2(self):
		# интерполяция за методом прогнозирования шага
		plt.axis('equal')
		plt.plot(self.list_x2_axis,self.list_y2_axis,c='b')
		plt.plot(self.inter_freq['x'], self.inter_freq['y'], 'o--', color='k')
		plt.title('Interpolation 2')
		plt.grid(True)
		plt.show()

	def plot_inter3(self):
		# интерполяция за методом прогнозирования шага
		plt.axis('equal')
		plt.plot(self.list_x2_axis,self.list_y2_axis,c='b')
		plt.plot(self.cor_for['x'], self.cor_for['y'], 'o--', color='k')
		plt.title('Interpolation 3')
		plt.grid(True)
		plt.show()
