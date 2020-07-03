import numpy as np




def CNOT(tableau, a, b):
	'''
	CNOT from control a to target b
	'''
	n = tableau.shape[0]//2
	if a >= n or b >= n:
		print('Gate error, there is no such qubit!')
	tableau[:, 2*n] = (tableau[:, 2*n] + tableau[:, a]*tableau[:, n+b]*(tableau[:, b] + tableau[:, n+a] + 1)%2)%2
	tableau[:, b] = (tableau[:, b] + tableau[:, a])%2
	tableau[:, n+a] =  (tableau[:, n+a] + tableau[:, n+b])%2
	return tableau




def Hadamard(tableau, a):
	'''
	Hadamard on qubit a
	'''
	n = tableau.shape[0]//2
	if a >= n:
		print('Gate error, there is no such qubit!')
	tableau[:, 2*n] = (tableau[:, 2*n] + tableau[:, a]*tableau[:, n+a])%2
	tableau[:, [a, n+a]] = tableau[:, [n+a, a]]
	return tableau




def Phase(tableau, a):
	'''
	Phase gate (S-gate) on qubit a
	'''
	n = tableau.shape[0]//2
	if a >= n:
		print('Gate error, there is no such qubit!')
	tableau[:, 2*n] = (tableau[:, 2*n] + tableau[:, a]*tableau[:, n+a])%2
	tableau[:, n+a] = (tableau[:, n+a] + tableau[:, a])%2
	return tableau