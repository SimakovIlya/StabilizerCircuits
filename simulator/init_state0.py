import numpy as np



def init_state0(n):
	'''
	Rerurn a tableau for a state |0>^n
	'''
	tableau = np.zeros((2*n, 2*n+1), dtype = np.int8)
	for i in range(2*n):
		tableau[i, i] = 1
	return(tableau)