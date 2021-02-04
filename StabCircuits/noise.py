import numpy as np
from .gates import *
from .rowsum import rowsum
from .measure import measure
from random import random, randint




def Xflip(tableau, q, p):
    if random() < p:
        tableau = X_gate(tableau, q)
    return tableau



def Yflip(tableau, q, p):
    if random() < p:
        tableau = Y_gate(tableau, q)
    return tableau




def Zflip(tableau, q, p):
    if random() < p:
        tableau = Z_gate(tableau, q)
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