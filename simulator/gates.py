import numpy as np





def X_gate(tableau, q):
    tableau[:, -1] ^= tableau[:, q + tableau.shape[0]//2]
    return tableau




def Y_gate(tableau, q):
    tableau[:, -1] ^= tableau[:, q] ^ tableau[:, q + tableau.shape[0]//2]
    return tableau




def Z_gate(tableau, q):
    tableau[:, -1] ^= tableau[:, q]
    return tableau




def Ry05_gate(tableau, q):
    '''
    Ry(0.5)
    '''
    tableau = Z_gate(tableau, q)
    tableau = Hadamard(tableau, q)
    return tableau




def Ry_05_gate(tableau, q):
    '''
    Ry(-0.5)
    '''
    tableau = Hadamard(tableau, q)
    tableau = Z_gate(tableau, q)
    return tableau



def Rx05_gate(tableau, q):
    '''
    Rx(0.5)
    '''
    tableau = Phase(tableau, q)
    tableau = Z_gate(tableau, q)
    tableau = Hadamard(tableau, q)
    tableau = Phase(tableau, q)
    tableau = Z_gate(tableau, q)
    return tableau




def Rx_05_gate(tableau, q):
    '''
    Rx(-0.5)
    '''
    tableau = Phase(tableau, q)
    tableau = Hadamard(tableau, q)
    tableau = Phase(tableau, q)
    return tableau




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