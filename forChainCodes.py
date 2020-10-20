def cycle(table, n, basis):
    # basis = '0', '1, '+', '-', 'i+', 'i-'
    if (n - 10)%8 != 0:
        print("Wrong n!!!")
    m_data = np.zeros((n//2), dtype=np.int8)
    m_ancilla = np.zeros((n//2), dtype=np.int8)
    
    even = np.arange(n//2)*2 # ancilla qubits
    odd = np.arange(n//2)*2 + 1 # data qubits
    
    # correction cycle
    for i in even:
        table = amplitude_damping(table, i, Tg1Q/2, T1)
        table = depolarize(table, i, p_plane, p_axis, p_plane)
        table = Hadamard_noise(table, i, ph)
    for i in even:
        table = amplitude_damping(table, i, Tg1Q/2 + Tg2Q/2, T1)
        table = amplitude_damping(table, i+1, Tg1Q + Tg2Q/2, T1)
        table = iSWAP(table, i, i+1)
        table = ZZ_noise(table, i, i+1, pZZ)
    for i in even:
        table = amplitude_damping(table, i, Tg1Q/2 + Tg2Q/2, T1)
        table = Phase(table, i)
        table = depolarize(table, i, p_plane, p_axis, p_plane)
        table = Hadamard_noise(table, i, ph)
    for i in odd:
        table = amplitude_damping(table, i, Tg1Q + Tg2Q, T1)
        table = amplitude_damping(table, i+1, Tg1Q/2 + Tg2Q/2, T1)
        table = iSWAP(table, i, (i+1)%n)
        table = ZZ_noise(table, i, (i+1)%n, pZZ)
    for i in even:
        table = amplitude_damping(table, i, Tg2Q, T1)
        table = amplitude_damping(table, i+1, Tg2Q, T1)
        table = iSWAP(table, i, i+1)
        table = ZZ_noise(table, i, i+1, pZZ)
    for i in even:
        table = amplitude_damping(table, i, Tg1Q/2 + Tg2Q/2, T1)
        table = Z_gate(table, i)
        table = depolarize(table, i, p_plane, p_axis, p_plane)
        table = Hadamard_noise(table, i, ph)
    for i in odd:
        table = amplitude_damping(table, i, Tg1Q + Tg2Q, T1)
        table = amplitude_damping(table, i+1, Tg1Q/2 + Tg2Q/2, T1)
        table = iSWAP(table, i, (i+1)%n)
        table = ZZ_noise(table, i, (i+1)%n, pZZ)
    for i in even:
        table = amplitude_damping(table, i, Tg2Q/2 + Tg1Q/2, T1)
        table = amplitude_damping(table, i+1, Tg2Q/2, T1)
        table = depolarize(table, i, p_plane, p_axis, p_plane)
        table = Hadamard_noise(table, i, ph)
        table = Phase(table, i+1)
        table = amplitude_damping(table, i, Tg1Q/2, T1)
        table = amplitude_damping(table, i+1, Tg1Q, T1)
        
        
        
    # ancilla measurement
    for i in even:
        table, m_ancilla[i//2] = measure(table, i)
        if m_ancilla[i//2] == -1:
            table = X_gate(table, i)
    
    # data measurement
    table_tmp = copy.copy(table)
    for i in odd:
        if basis == '+' or basis == '-':
            table_tmp = Ry_05_gate(table_tmp, i)
        elif basis == 'i+' or basis == 'i-':
            table_tmp = Rx05_gate(table_tmp, i)
        table_tmp, m_data[(i-1)//2] = measure(table_tmp, i)
    
    for i in range(n):
        table = amplitude_damping(table, i, tm+td, T1)
        
    return table, m_data.astype(np.int8), m_ancilla.astype(np.int8)




def full_Cycle(proc_num, table=table, N=N, N_cycle=N_cycle):
    M_datanomeas = np.zeros((N_cycle, N//2), dtype = np.int8)
    M_ancillanomeas = np.zeros((N_cycle, N//2), dtype = np.int8)       
    for n_cycle in range(0, N_cycle):
        table, M_datanomeas[n_cycle], M_ancillanomeas[n_cycle] = cycle(table, N, basis)
    return [M_datanomeas, M_ancillanomeas]