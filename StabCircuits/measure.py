import numpy as np
from .rowsum import rowsum
from random import randint, random
from .gates import X_gate





def measure(tableau, a, eta = np.array([[1, 1, 1], [0, 0, 0]])):
    '''
    Measurement of qubit a in standard basis

    Returns:
        tableau
        measurement_outcome (1 or -1)
    '''

    # # ideal case
    # n = tableau.shape[0]//2
    # nonzero_elements = np.nonzero(tableau[n:2*n, a])[0] + n
    # if nonzero_elements.shape[0] == 0:
    #     # case 2
    #     # the outcome is determinate, so measuring the state will not change it
    #     tableau_tmp = np.vstack((tableau, np.zeros((2*n + 1), dtype = np.int8)))
    #     for i in np.nonzero(tableau[:n, a])[0]:
    #         tableau_tmp = rowsum(tableau_tmp, 2*n, i+n)
    #     measurement_outcome = -(tableau_tmp[2*n, 2*n]*2-1)
    # else:
    #     # case 1
    #     # the measurement outcome is random, so the state needs to be updated
    #     p = nonzero_elements[0]
    #     for i in np.nonzero(tableau[:2*n, a])[0]:
    #         if i != p and i != p-n:
    #             tableau = rowsum(tableau, i, p)
    #     tableau[p-n, :] = tableau[p, :]
    #     tableau[p, :] = 0
    #     tableau[p, 2*n] = randint(0, 1)
    #     tableau[p, n+a] = 1
    #     measurement_outcome = -(tableau[p, 2*n]*2-1)

    # # add error
    # tmp = random()
    # if measurement_outcome == 1:
    #     if tmp > eta[0, 0]:
    #         if tmp < eta[0, 1]:
    #             tableau = X_gate(tableau, a)
    #         elif tmp < eta[0, 2]:
    #             measurement_outcome *= -1
    #         else:
    #             tableau = X_gate(tableau, a)
    #             measurement_outcome *= -1
    # elif measurement_outcome == -1:
    #     if tmp < eta[1, 2]:
    #         if tmp < eta[1, 1]:
    #             tableau = X_gate(tableau, a)
    #         elif tmp < eta[1, 0]:
    #             measurement_outcome *= -1
    #         else:
    #             tableau = X_gate(tableau, a)
    #             measurement_outcome *= -1

    # # Good bellow
    n = tableau.shape[0]//2
    nonzero_elements = np.nonzero(tableau[n:2*n, a])[0] + n
    if nonzero_elements.shape[0] == 0:
        # case 2
        # the outcome is determinate, so measuring the state will not change it
        tableau_tmp = np.vstack((tableau, np.zeros((2*n + 1), dtype = np.int8)))
        for i in np.nonzero(tableau[:n, a])[0]:
            tableau_tmp = rowsum(tableau_tmp, 2*n, i+n)

        p_in = tableau_tmp[2*n, 2*n]
        p_out = random()
        if p_in == 0:
            if p_out <= eta[0, 0]:
                m = 1
            elif p_out <= eta[0, 1]:
                m = 1
                tableau = X_gate(tableau, a)
            elif p_out <= eta[0, 2]:
                m = -1
            else:
                m = -1
                tableau = X_gate(tableau, a)
        elif p_in == 1:
            if p_out <= eta[1, 0]:
                m = 1
                tableau = X_gate(tableau, a)
            elif p_out <= eta[1, 1]:
                m = 1
            elif p_out <= eta[1, 2]:
                m = -1
                tableau = X_gate(tableau, a)
            else:
                m = -1
        measurement_outcome = m
        # measurement_outcome = -(tableau_tmp[2*n, 2*n]*2-1)
    else:
        # case 1
        # the measurement outcome is random, so the state needs to be updated
        p = nonzero_elements[0]
        for i in np.nonzero(tableau[:2*n, a])[0]:
            if i != p and i != p-n:
                tableau = rowsum(tableau, i, p)
        tableau[p-n, :] = tableau[p, :]
        tableau[p, :] = 0

        # tableau[p, 2*n] = randint(0, 1)

        p_in = randint(0, 1)
        p_out = random()
        if p_out <= eta[p_in, 0]:
            m = 1
            tableau[p, 2*n] = 0
        elif p_out <= eta[p_in, 1]:
            m = 1
            tableau[p, 2*n] = 1
        elif p_out <= eta[p_in, 2]:
            m = -1
            tableau[p, 2*n] = 0
        else:
            m = -1
            tableau[p, 2*n] = 1
            
        tableau[p, n+a] = 1
        # measurement_outcome = -(tableau[p, 2*n]*2-1)
        measurement_outcome = m

    return tableau, measurement_outcome