from .basic_gates import *



def X_gate(tableau, a):
	'''
	X_gate (NOT) on qubit a
	'''
	if a >= tableau.shape[0]//2:
		print('Gate error, there is no such qubit!')
	tableau = Hadamard(tableau, a)
	tableau = Z_gate(tableau, a)
	tableau = Hadamard(tableau, a)
	return tableau


def Z_gate(tableau, a):
	'''
	Z_gate on qubit a
	'''
	if a >= tableau.shape[0]//2:
		print('Gate error, there is no such qubit!')
	return Phase(Phase(tableau, a), a)


def iSWAP(tableau, a, b):
	'''
	iSWAP between qubits a, b
	'''
	if a >= tableau.shape[0]//2 or b >= tableau.shape[0]//2:
		print('Gate error, there is no such qubit!')
	tableau = Phase(tableau, a)
	tableau = Phase(tableau, b)
	tableau = Hadamard(tableau, a)
	tableau = CNOT(tableau, a, b)
	tableau = CNOT(tableau, b, a)
	tableau = Hadamard(tableau, b)
	return tableau