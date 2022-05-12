import numpy as np
import networkx as nx

def binary(num):
    return np.array([int(digit) for digit in bin(num)[2:]]) # [2:] to chop off the "0b" part 

# ***** Q1 *****
# strategy: 
def q1(n):
    print('q1')
    adj = np.zeros((n,n))
    for i in range(2^(n*n)):
        mat = binary(i).reshape((n,n))
        print(mat)




# ***** Q2 *****


# **** MAIN ****
n = 2
q1(n)
