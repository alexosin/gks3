import numpy as np

def built_equatation(matrix, letter, header):
	print('{:-^30}'.format(header))
	p_inz = []
	for i in matrix.tolist():
		egg = ''
		for u, j in enumerate(i):
			if j == 0:
				continue
			key = '+' if j > 0 else '-'
			if not egg:
				key = ''
			egg = egg + key + letter + str(u+1)
		egg += '=0'
		p_inz.append(egg)
	for i in p_inz:
		print(' '*10 + i)
	rank = np.linalg.matrix_rank(matrix)
	print('  ранг матрицы = ', rank)
	if rank == u+1:
		print('   нулевое решение ', np.linalg.lstsq(matrix, np.zeros(len(matrix)))[0])
	elif rank < u+1:
		print('   система имеет одно базисное решение\n     при  x1 = 1')
		x1 = [-i*1 for i in matrix[:,0]]
		matrix = [i[1:] for i in matrix]
		print(' '*10, np.linalg.lstsq(matrix, x1)[0])
	print()

def main():
	F = np.array([[0, 1, 0],
					[0, 1, 0],
					[1, 0, 0],
					[0, 0, 1]])

	H = np.array([[1, 0, 1],
					[1, 0, 1],
					[0, 1, 0],
					[0, 1, 0]])

	M0 = np.array([1, 1, 0, 0])

	A = H - F
	At = np.transpose(A)

	equat = built_equatation(At, 'x', 'P-инварианта')
	equat = built_equatation(A, 'y', 'T-инварианта')

if __name__=="__main__":
	main()
