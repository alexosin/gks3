import numpy as np
import matplotlib.pyplot as plt
from os import path
from sys import argv

def gantt_draw(filename):
	# Read data from file into variables
	y, c, x1, x2 = np.loadtxt(str(path.realpath(path.dirname(argv[0]))) + '/datafile/' + filename + '.txt', unpack=True)
	# Map value to color
	color_mapper = np.vectorize(lambda x: {0: 'red', 1: 'blue', 2:'green', 3:'m', 4:'grey'}.get(x))

	# Plot a line for every line of data in your file
	plt.xlabel('Time (red - first oper, blue - second, green - third, magenta - fourth)')
	plt.ylabel('Equipment( 5(1) - first, 10(2) - second, 15(3) - third)')
	plt.grid(linewidth=3)
	plt.title('Gantt chart ' + filename)
	plt.hlines(y, x1, x2, colors=color_mapper(c), linewidths=20)
	plt.savefig(str(path.realpath(path.dirname(argv[0]))) + '/img/' + filename + '.png')
	plt.clf()
