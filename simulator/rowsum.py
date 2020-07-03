import numpy as np



def rowsum(tableau, h, i):
	n = tableau.shape[1] - 1
	s = 2*tableau[h, n] + 2*tableau[i, n] +\
		np.sum(g_func_table[tableau[i,:n//2], tableau[i,n//2:n], tableau[h,:n//2], tableau[h,n//2:n]])
	if s%4 == 0:
		tableau[h, n] = 0
	elif s%4 == 2:
		tableau[h, n] = 1
	else:
		print ('error in rowsum', h, i)
	tableau[h, :n] = (tableau[h, :n] + tableau[i, :n])%2
	return(tableau)

	


def g_func(x1, z1, x2, z2):
	if x1 == z1:
		if x1 == 0:
			return 0
		else:
			return (z2 - x2)
	elif x1 == 1:
		return (z2 * (2*x2 - 1))
	else:
		return (x2 * (1 - 2*z2))




g_func_table = np.zeros((2, 2, 2, 2), dtype = np.int8)
for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                g_func_table[i, j, k, l] = g_func(i, j, k, l)