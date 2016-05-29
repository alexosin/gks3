import matplotlib.pyplot as plt
import math

class LinePath:
	def __init__(self, start=(0, 0), end=(0, 0), angle=0, length=0,
				leading='x', secondary='y'):
		self.start = start
		self.end = end
		self.angle = angle
		self.length = length
		self.endx, self.endy = end

	def get_endpoint_by_angle(self):
		# метод для нахождения конечной точки прямой под заданым углом
		x1, y1 = self.start
		x2, y2 = self.endx, self.endy
		if not self.length:
			self.length = math.sqrt((x2-x1)**2 + (y2-y1)**2)

		self.endx = x1 + self.length * math.cos(math.radians(self.angle))#)
		self.endy = y1 + self.length * math.sin(math.radians(self.angle))#)

	def get_line_func(self):
		# метод для нахождение коэффициентов функции прямой
		x1, y1 = self.start
		x2, y2 = self.endx, self.endy
		self.k = (y1 - y2) / (x1 - x2)
		self.b = y2 - self.k * x2


	def get_leading_axis(self):
		# метод для определение ведущей оси
		if self.angle <= 45:
			self.leading = 'x'
		elif self.angle > 45:
			self.leading = 'y'

	def get_path_by_interpolation_predict(self, step, plotted=False):
		# метод для построения траектории с помощью линейной интерполяции
		# оценночной функции с прогнозированием шага
		x_points, y_points = [], []
		x_points.append(self.start[0])
		y_points.append(self.start[1])
		self.get_leading_axis()
		if self.leading == 'x':
			x = self.start[0] + step
			y = self.start[1]
			x_points.append(x)
			y_points.append(y)
			for i in range(int(self.X / step)):
				if y >= (self.k * x + self.b):
					x = x + step
				else:
					x = x + step
					y = y + step
				x_points.append(x)
				y_points.append(y)
		elif self.leading == 'y':
			x = self.start[0]
			y = self.start[1] + step
			x_points.append(x)
			y_points.append(y)
			for i in range(int(self.Y / step)):
				if x >= (y - self.b) / self.k:
					y = y + step
				else:
					x = x + step
					y = y + step
				x_points.append(x)
				y_points.append(y)
		x_points.append(self.endx)
		y_points.append(self.endy)
		self.inter_predict = {'x2': x_points, 'y2': y_points}
		if self.leading == 'x':
			x_points = list(map(lambda i: i - 1, x_points[1:-1]))
			x_points.append(self.endx)
			x_points.insert(0, self.start[0])
		else:
			y_points = list(map(lambda i: i - 1, y_points[1:-1]))
			y_points.append(self.endy)
			y_points.insert(0, self.start[1])
		self.inter_predict['x'] = x_points
		self.inter_predict['y'] = y_points
		if plotted:
			self.plot_inter1()

	def calc_parametr(self, T, V, step, plotted=False):
		# расчитуем начальные данные для построения траектории методом на
		# несучей частоте ЦДА
		self.T = T
		self.V = V
		self.step = step
		self.X = self.endx-self.start[0]
		self.Y = self.endy-self.start[1]
		self.tau = math.sqrt(self.X**2 + self.Y**2) / self.V
		self.imax = math.floor(self.tau / self.T)
		self.delta_x = (self.X * self.T) / self.tau
		self.delta_y = (self.Y * self.T) / self.tau
		self.delta_x1 = int(self.delta_x / step) * step
		self.delta_y1 = int(self.delta_y / step) * step
		if plotted:
			print('delta_x = {}, delta_y = {}'.format(self.delta_x, self.delta_y))
			print('delta_x_step = {}, delta_y_step = {}'.format(self.delta_x1, self.delta_y1))

	def method_cont_carrier_freq(self, plotted = False):
		# метод оценочной функции на постоянной несущей частоте
		x_points, y_points = [], []
		x_growth, y_growth = [], []
		sum_delta_x = 0
		sum_delta_y = 0

		# считаем приросты по осям
		if plotted:
			print('\nFrequence Interpolation')
		for i in range(1, self.imax):
			N = sum_delta_x + self.delta_x1 - i * self.delta_x
			M = sum_delta_y + self.delta_y1 - i * self.delta_y
			dx = self.delta_x1 if N > 0 else self.delta_x1 + self.step
			sum_delta_x += dx
			x_growth.append(dx)
			dy = self.delta_y1 if M > 0 else self.delta_y1 + self.step
			sum_delta_y += dy
			y_growth.append(dy)
			if plotted:
				print('N = {}, x = {}, M = {}, y = {}'.format(N, dx, M, dy))
		dx = self.X - sum_delta_x
		dy = self.Y - sum_delta_y
		if dx and dy:
			x_growth.append(dx)
			y_growth.append(dy)

		# находим точки для построения траектории
		x_points.append(self.start[0])
		y_points.append(self.start[1])
		for i in range(len(x_growth)):
			x_points.append(x_points[-1] + x_growth[i])
			y_points.append(y_points[-1] + y_growth[i])
		self.inter_freq = {'x': x_points[1:], 'y': y_points[1:]}
		if plotted:
			self.plot_inter2()

	def CDA(self, plotted=False):
		# метод цифрового дифференциального анализатора
		x_points, y_points = [], []
		x_growth, y_growth = [], []
		x_balance = 0
		y_balance = 0
		sum_delta_x = 0
		sum_delta_y = 0
		if plotted:
			print('\nCDA Interpolation')
		for i in range(1, self.imax):
			x_full = self.delta_x + x_balance
			y_full = self.delta_y + y_balance
			dx = int(x_full / self.step) * self.step
			dy = int(y_full / self.step) * self.step
			x_balance = x_full - dx
			y_balance = y_full - dy
			sum_delta_x += dx
			sum_delta_y += dy
			x_growth.append(dx)
			y_growth.append(dy)
			if plotted:
				print('xf = {}, yf = {}, dx = {}, dy = {}, xb = {} , yb = {}' \
				.format(x_full, y_full, dx, dy, x_balance, y_balance))

		dx = self.X - sum_delta_x
		dy = self.Y - sum_delta_y
		if dx and dy:
			x_growth.append(dx)
			y_growth.append(dy)

		x_points.append(self.start[0])
		y_points.append(self.start[1])
		for i in range(len(x_growth)):
			x_points.append(x_points[-1] + x_growth[i])
			y_points.append(y_points[-1] + y_growth[i])
		self.inter_cda = {'x': x_points[1:], 'y': y_points[1:]}
		if plotted:
			self.plot_inter3()

	def find_distance(self, M):
		x1, y1 = self.start
		x2, y2 = self.endx, self.endy
		A = y1 - y2
		B = x2 - x1
		C = x1 * y2 - x2 * y1
		d = abs(A*M[0] + B*M[1] + C) / (math.sqrt(A**2 + B**2))
		return round(d, 5)

	def plot_inter1(self):
		# интерполяция за методом прогнозирования шага
		plt.plot([self.start[0], self.endx], [self.start[1], self.endy])
		plt.plot(self.inter_predict['x'], self.inter_predict['y'], '--', color='r')
		plt.plot(self.inter_predict['x2'], self.inter_predict['y2'], '-', color='k')
		plt.title('Interpolation 1')
		plt.axis([self.start[0]-1, self.endx+1, self.start[1]-1, self.endy+1])
		plt.grid(True)
		plt.show()

	def plot_inter2(self):
		# интерполяция за методом на постоянной несущей частоте
		plt.plot([self.start[0], self.endx], [self.start[1], self.endy])
		plt.plot(self.inter_freq['x'], self.inter_freq['y'], 'o', color='r')
		plt.title('Interpolation 2')
		plt.axis([self.start[0]-1, self.endx+1, self.start[1]-1, self.endy+1])
		plt.grid(True)
		plt.show()

	def plot_inter3(self):
		# интерполяция за методом на постоянной несущей частоте
		plt.plot([self.start[0], self.endx], [self.start[1], self.endy])
		plt.plot(self.inter_cda['x'], self.inter_cda['y'], 'o', color='r')
		plt.title('Interpolation 3')
		plt.axis([self.start[0]-1, self.endx+1, self.start[1]-1, self.endy+1])
		plt.grid(True)
		plt.show()
