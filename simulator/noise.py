import numpy as np
from .gates import *
from .measure import measure
from random import random




def amplitude_damping(tableau, q, t, T1):
    if random() < 1-np.exp(-t/2/T1):
    	# for i in range(3):
    	# 	tableau_tmp, m = measure(tableau.copy(), q)
    	# 	if m == 1:
     #    		tableau = X_gate(tableau, q)
     #    		break
     	tableau = X_gate(tableau, q)
    return tableau




def phase_damping(tablau, q, t, T2):
    return tableau




def depolarize(tableau, q, px, py, pz):
	r = random()
	if r < px:
		tableau = X_gate(tableau, q)
	elif r < px+py:
		tableau = Y_gate(tableau, q)
	elif r < px+py+pz:
		tableau = Z_gate(tableau, q)
	return tableau



def Hadamard_noise(tableau, q, p):
	'''
	Hadamrd on qubit q with noise channels probabilities p and p (ideal probability = 1-2p)
	H = Y(1/2)*Z
	Z - always ideal
	Y(1/2) = (1-2p)*Y(1/2) + p*I + p*Y
 	'''
	r = random()
	if r < p:
		tableau = Z_gate(tableau, q)
	elif r < p+p:
		tableau = Y_gate(tableau, q)
		tableau = Z_gate(tableau, q)
	else:
		tableau = Hadamard(tableau, q)
	return tableau




def ZZ_noise(tableau, q1, q2, p):
	'''
	ZZ noise between qubits q1 and q2  (+-S gates on q1 and q2 with probabilities p)
	'''
	r = random()
	if r < p:
		if random() < 1/2:
			tableau = Phase(tableau, q1)
		else:
			tableau = Phase(tableau, q1)
			tableau = Phase(tableau, q1)
			tableau = Phase(tableau, q1)
	r = random()
	if r < p:
		if random() < 1/2:
			tableau = Phase(tableau, q2)
		else:
			tableau = Phase(tableau, q2)
			tableau = Phase(tableau, q2)
			tableau = Phase(tableau, q2)
	return tableau




def add_noise_to_measurements(meas, p0, p1):
	'''
	p0 - probability 1 -> -1 (0 -> 1) 
	p1 - probability -1 -> 1 (1 -> 0)
	'''
	m = meas.copy()
	for i in range(m.shape[0]):
		for j in range(m.shape[1]):
			for k in range(m.shape[2]):
				r = random()
				if m[i, j, k] == 1 and r < p0:
					m[i, j, k] = -1
				elif m[i, j, k] == -1 and r < p1:
					m[i, j, k] = 1
	return m










