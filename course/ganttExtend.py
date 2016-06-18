import matplotlib.pyplot as plt
import sys
import numpy as np
import operator
import os
import matplotlib.patches as mpatches

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

extend_gantt_draw('extendGantt')
