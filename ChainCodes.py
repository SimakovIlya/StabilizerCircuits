from StabCircuits import *
import numpy as np
from copy import copy




class ChainCodes:
    def __init__(self, args):
        self.T1 = args['T1']
        self.Tf = args['Tf']
        self.Tg1Q = args['Tg1Q']
        self.Tg2Q = args['Tg2Q']
        self.tm = args['tm']
        self.td = args['td']
        self.p_axis = args['p_axis']
        self.p_plane = args['p_plane']
        self.ph = args['ph']
        self.pZZ = args['pZZ']
        self.p0 = args['p0']
        self.p1 = args['p1']




    def cycle(self, table, n, basis):
        # basis = '0', '1, '+', '-', 'i+', 'i-'
        if (n - 10)%8 != 0:
            print("Wrong n!!!")
        m_data = np.zeros((n//2), dtype=np.int8)
        m_ancilla = np.zeros((n//2), dtype=np.int8)
        
        even = np.arange(n//2)*2 # ancilla qubits
        odd = np.arange(n//2)*2 + 1 # data qubits
        
        # correction cycle
        for i in even:
            table = amplitude_damping(table, i, self.Tg1Q/2, self.T1)
            table = depolarize(table, i, self.p_plane, self.p_axis, self.p_plane)
            table = Hadamard_noise(table, i, self.ph)
        for i in even:
            table = amplitude_damping(table, i, self.Tg1Q/2 + self.Tg2Q/2, self.T1)
            table = amplitude_damping(table, i+1, self.Tg1Q + self.Tg2Q/2, self.T1)
            table = iSWAP(table, i, i+1)
            table = ZZ_noise(table, i, i+1, self.pZZ)
        for i in even:
            table = amplitude_damping(table, i, self.Tg1Q/2 + self.Tg2Q/2, self.T1)
            table = Phase(table, i)
            table = depolarize(table, i, self.p_plane, self.p_axis, self.p_plane)
            table = Hadamard_noise(table, i, self.ph)
        for i in odd:
            table = amplitude_damping(table, i, self.Tg1Q + self.Tg2Q, self.T1)
            table = amplitude_damping(table, i+1, self.Tg1Q/2 + self.Tg2Q/2, self.T1)
            table = iSWAP(table, i, (i+1)%n)
            table = ZZ_noise(table, i, (i+1)%n, self.pZZ)
        for i in even:
            table = amplitude_damping(table, i, self.Tg2Q, self.T1)
            table = amplitude_damping(table, i+1, self.Tg2Q, self.T1)
            table = iSWAP(table, i, i+1)
            table = ZZ_noise(table, i, i+1, self.pZZ)
        for i in even:
            table = amplitude_damping(table, i, self.Tg1Q/2 + self.Tg2Q/2, self.T1)
            table = Z_gate(table, i)
            table = depolarize(table, i, self.p_plane, self.p_axis, self.p_plane)
            table = Hadamard_noise(table, i, self.ph)
        for i in odd:
            table = amplitude_damping(table, i, self.Tg1Q + self.Tg2Q, self.T1)
            table = amplitude_damping(table, i+1, self.Tg1Q/2 + self.Tg2Q/2, self.T1)
            table = iSWAP(table, i, (i+1)%n)
            table = ZZ_noise(table, i, (i+1)%n, self.pZZ)
        for i in even:
            table = amplitude_damping(table, i, self.Tg2Q/2 + self.Tg1Q/2, self.T1)
            table = amplitude_damping(table, i+1, self.Tg2Q/2, self.T1)
            table = depolarize(table, i, self.p_plane, self.p_axis, self.p_plane)
            table = Hadamard_noise(table, i, self.ph)
            table = Phase(table, i+1)
            table = amplitude_damping(table, i, self.Tg1Q/2, self.T1)
            table = amplitude_damping(table, i+1, self.Tg1Q, self.T1)

        # ancilla measurement
        for i in even:
            table, m_ancilla[i//2] = measure(table, i)
            if m_ancilla[i//2] == -1:
                table = X_gate(table, i)
        
        # data measurement
        table_tmp = copy(table)
        for i in odd:
            if basis == '+' or basis == '-':
                table_tmp = Ry_05_gate(table_tmp, i)
            elif basis == 'i+' or basis == 'i-':
                table_tmp = Rx05_gate(table_tmp, i)
            table_tmp, m_data[(i-1)//2] = measure(table_tmp, i)
        
        for i in range(n):
            table = amplitude_damping(table, i, self.tm+self.td, self.T1)
            
        return table, m_data.astype(np.int8), m_ancilla.astype(np.int8)




    def set_full_Cycle(self, table, N, N_cycle, basis):
        self.table = table
        self.N = N
        self.N_cycle = N_cycle
        self.basis = basis




    def full_Cycle(self, proc_num):
        M_datanomeas = np.zeros((self.N_cycle, self.N//2), dtype = np.int8)
        M_ancillanomeas = np.zeros((self.N_cycle, self.N//2), dtype = np.int8)       
        for n_cycle in range(0, self.N_cycle):
            table, M_datanomeas[n_cycle], M_ancillanomeas[n_cycle] = self.cycle(self.table, self.N, self.basis)
        return [M_datanomeas, M_ancillanomeas]