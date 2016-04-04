import numpy as np
import matplotlib.pyplot as plt
from os import path
from sys import argv

def gantt_draw(filename):
	# Read data from file into variables
	y, c, x1, x2 = np.loadtxt(str(path.realpath(path.dirname(argv[0]))) + '/datafile/' + filename + '.txt', unpack=True)
	# Map value to color
	color_mapper = np.vectorize(lambda x: {0: 'red', 1: 'blue', 2:'green', 3:'m'}.get(x))

	# Plot a line for every line of data in your file
	plt.hlines(y, x1, x2, colors=color_mapper(c), linewidths=10)
	plt.xlabel('Time')
	plt.ylabel('Equipment( 5 - first, 10 - second, 15 - third)')
	plt.grid(linewidth=2)
	plt.title('Gantt chart')
	plt.savefig(str(path.realpath(path.dirname(argv[0]))) + 'img/' + filename + '.png')
