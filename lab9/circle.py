import matplotlib.pyplot as plt
import math
import sys
sys.path.append(sys.argv[0][:-14])
from lab8 import line

class CirclePath:
	def __init__(self, center, radius, angle_degrees=(0, 90)):
		# center - (centerX, centerY)
		# angle_degrees - (start, end) work only with (0, 90)
		self.centerX = center[0]
		self.centerY = center[1]
		self.radius = radius
		self.angle_degrees = angle_degrees
		self.calc_parameter()
		self.start = (self.centerX+radius, self.centerY)
		self.end = (self.centerX, self.centerY + self.radius)

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
		print(self.bisector.endx, self.bisector.endy)

	def plot_circle(self):
		plt.axis('equal')
		plt.grid()
		plt.plot([self.bisector.start[0], self.bisector.endx],
				[self.bisector.start[1], self.bisector.endy], '--')
		plt.plot(self.list_x2_axis,self.list_y2_axis,c='b')
		plt.show()

	def get_distance_between_center_and_point(self, pointX, pointY):
		# найти расстояние между жвумя точками
		return math.sqrt((pointX-self.centerX)**2 + (pointY-self.centerY)**2)

	def get_path_by_interpolation_predict(self, step, plotted=False):
		# метод для построения траектории с помощью линейной интерполяции
		# оценночной функции с прогнозированием шага
		x_points, y_points = [], []
		x_points.append(self.start[0])
		y_points.append(self.start[1])
		x = self.start[0] - step
		y = self.start[1] + step
		x_points.append(x)
		y_points.append(y)
		print(self.bisector.endx)
		while x >= (y - self.bisector.b) / self.bisector.k:
			print(x, y)
			if self.get_distance_between_center_and_point(x, y) >= self.radius:
				print(True)
				x = x - step
				y = y + step
			else:
				y = y + step
			x_points.append(x)
			y_points.append(y)
		while x >= self.end[0]:
			if self.get_distance_between_center_and_point(x, y) >= self.radius:
				x = x - step
			else:
				x = x - step
				y = y + step
			x_points.append(x)
			y_points.append(y)
		self.inter_predict = {'x2': x_points, 'y2': y_points}
		x_points = [i + 1 for i in x_points[1:]]
		y_points = [i - 1 for i in y_points[1:]]
		x_points.append(self.end[0])
		y_points.append(self.end[1])
		self.inter_predict['x'] = x_points
		self.inter_predict['y'] = y_points
		if plotted:
			self.plot_inter()

	def plot_inter(self):
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
