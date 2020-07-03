import numpy as np



def get_stabilizers(tableau):
    '''
    Returns stabilizers (0..n) and destabilizers (n..2n) from the tableau
    '''
    n = tableau.shape[0]//2
    stab_list = ['']*2*n
    P_list = [['I', 'X'],['Z', 'Y']]
    for i in range(2*n):
        if tableau[i, 2*n] == 0:
            s = '+'
        else:
            s = '-'
        for j in range(n):
            s = s + P_list[tableau[i, j]][tableau[i, n+j]]
        stab_list[i] = s
    return(stab_list)