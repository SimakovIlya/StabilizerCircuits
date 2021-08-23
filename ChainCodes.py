from StabCircuits import *
import numpy as np
from copy import copy
from random import random




class ChainCodes:
    def __init__(self, args):
        self.T1 = args['T1']
        self.Tf = args['Tf']
        self.Tg1Q = args['Tg1Q']
        self.Tg2Q = args['Tg2Q']
        self.tm = args['tm']
        self.td = args['td']
        self.eta = args['eta']
        # self.p_axis = args['p_axis']
        # self.p_plane = args['p_plane']
        
        
    
    
    def damping(self, table, q, t):
        if random() < 1-np.exp(-t/self.T1/2):
            table = X_gate(table, q)
        if random() < 1-np.exp(-t/self.T1/2):
            table = Y_gate(table, q)
        if random() < 1-np.exp(-t/self.Tf):
            table = Z_gate(table, q)
        return table
    



    def cycle(self, table, n, basis):
        # basis = '0', '1, '+', '-', 'i+', 'i-'
        if (n - 10)%8 != 0:
            print("Wrong n!!!")
        m_data = np.zeros((n//2), dtype=np.int8)
        m_ancilla = np.zeros((n//2), dtype=np.int8)
        m_data_ideal = np.zeros((n//2), dtype=np.int8)
        m_ancilla_ideal = np.zeros((n//2), dtype=np.int8)
        
        even = np.arange(n//2)*2 # ancilla qubits
        odd = np.arange(n//2)*2 + 1 # data qubits
        
        # correction cycle
        for i in even:
            table = self.damping(table, i, self.Tg1Q/2)
            table = Hadamard(table, i)
        for i in even:
            table = self.damping(table, i, self.Tg1Q/2 + self.Tg2Q/2)
            table = self.damping(table, i+1, self.Tg1Q + self.Tg2Q/2)
            table = iSWAP(table, i, i+1)
        for i in even:
            table = self.damping(table, i, self.Tg1Q/2 + self.Tg2Q/2)
            table = Phase(table, i)
            table = Hadamard(table, i)
        for i in odd:
            table = self.damping(table, i, self.Tg1Q + self.Tg2Q)
            table = self.damping(table, i+1, self.Tg1Q/2 + self.Tg2Q/2)
            table = iSWAP(table, i, (i+1)%n)
        for i in even:
            table = self.damping(table, i, self.Tg2Q)
            table = self.damping(table, i+1, self.Tg2Q)
            table = iSWAP(table, i, i+1)
        for i in even:
            table = self.damping(table, i, self.Tg1Q/2 + self.Tg2Q/2)
            table = Z_gate(table, i)
            table = Hadamard(table, i)
        for i in odd:
            table = self.damping(table, i, self.Tg1Q + self.Tg2Q)
            table = self.damping(table, i+1, self.Tg1Q/2 + self.Tg2Q/2)
            table = iSWAP(table, i, (i+1)%n)
        for i in even:
            table = self.damping(table, i, self.Tg2Q/2 + self.Tg1Q/2)
            table = self.damping(table, i+1, self.Tg2Q/2)
            table = Hadamard(table, i)
            table = Phase(table, i+1)
            table = self.damping(table, i, self.Tg1Q/2)
            table = self.damping(table, i+1, self.Tg1Q)

            

        # ancilla measurement
        for i in even:
            table, m_ancilla[i//2] = measure(table, i, self.eta)
            table, m = measure(table, i)
            if m == -1:
                table = X_gate(table, i)
        
        # data measurement
        table_tmp = copy(table)
        table_tmp_ideal = copy(table)
        for i in odd:
            if basis == '+' or basis == '-':
                table_tmp = Ry_05_gate(table_tmp, i)
                table_tmp_ideal = Ry_05_gate(table_tmp_ideal, i)
            elif basis == 'i+' or basis == 'i-':
                table_tmp = Rx_05_gate(table_tmp, i)
                table_tmp_ideal = Rx05_gate(table_tmp_ideal, i)

            table_tmp, m_data[(i-1)//2] = measure(table_tmp, i, self.eta)
            table_tmp_ideal, m_data_ideal[(i-1)//2] = measure(table_tmp_ideal, i)
        
        for i in odd:
            table = self.damping(table, i, self.tm+self.td)
            
            
        return table, m_data_ideal.astype(np.int8), m_data.astype(np.int8), m_ancilla.astype(np.int8)




    def set_full_Cycle(self, table, N, N_cycle, basis):
        self.table = table
        self.N = N
        self.N_cycle = N_cycle
        self.basis = basis




    def full_Cycle(self, proc_num):
        M_data_ideal = np.zeros((self.N_cycle, self.N//2), dtype = np.int8)
        M_data = np.zeros((self.N_cycle, self.N//2), dtype = np.int8)
        M_ancilla = np.zeros((self.N_cycle, self.N//2), dtype = np.int8)
        for n_cycle in range(0, self.N_cycle):
            table, M_data_ideal[n_cycle],\
                   M_data[n_cycle], M_ancilla[n_cycle] = self.cycle(self.table, self.N, self.basis)
        return [M_data_ideal, M_data, M_ancilla]