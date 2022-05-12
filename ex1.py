import numpy as np
import networkx as nx
from itertools import combinations


def binary(n, N):  # n value with N bits
    dst = np.zeros(N * N)
    bin_list = [int(digit) for digit in bin(n)[2:]]  # [2:] to chop off the "0b" part
    bin_list = [0] * (N * N - len(bin_list)) + bin_list
    return np.array(bin_list)


def is_new(new, g_list):
    for g in g_list:
        if nx.is_isomorphic(new, g):
            return False
    return True


def count_motifs(motif, subgraphs):
    count = 0
    motif = nx.DiGraph(motif)
    for subgraph in subgraphs:
        if nx.is_isomorphic(motif, nx.DiGraph(subgraph)):
            count += 1
    return count


def get_subgraphs(adj, n):
    subgraphs = []
    # get any combination of n vertices sub graph
    for comb in combinations(range(adj.shape[0]), n):
        subgraphs.append(adj[np.ix_(comb, comb)])
    return subgraphs


# ***** Q1 *****
def q1(n, to_file=True):
    # get subgraphs list
    count = 0
    subgraphs = []
    adj = np.zeros((n, n))
    for i in range(1, 2**(n*n)):
        mat = binary(i, n).reshape((n, n))
        G = nx.DiGraph(mat)
        # force diagonal 0 (no self edges), connectivity = at least n-1 edges
        if np.sum(mat) < (n-1) or 0 != np.trace(mat):
            continue
        if nx.is_weakly_connected(G) and is_new(G, subgraphs):
            subgraphs.append(G)
    if 1 == n:  # special case - self edges allowed
        subgraphs.append(nx.DiGraph(np.array([[1]])))

    # save to file
    if to_file:
        str_graphs = ''
        for idx, g in enumerate(subgraphs):
            str_graphs += '#' + str(idx+1) + '\n'
            mat = nx.to_numpy_array(g)
            for i in range(n):
                for j in range(n):
                    if 1 == mat[i, j]:
                        str_graphs += str(i+1) + ' ' + str(j+1) + '\n'

        fname = 'sub-graphs_n' + str(n) + '.txt'
        f = open(fname, 'w')
        data = 'n=' + str(n) + '\n'
        data += 'count=' + str(count) + '\n'
        data += str_graphs
        f.write(data)
        f.close()

    return subgraphs


# ***** Q2 *****
def q2(fname, n):
    # read file
    f = open(fname, 'r')
    data = f.read().splitlines()  # edges list
    f.close()

    # make adjacency matrix
    # assuming all vertices numbered from 1 to len(vertices)
    nodes = [node.split(' ') for node in data]  # split to nodes
    nodes = np.array([list(map(int, node)) for node in nodes])  # nodes as integers
    num_v = nodes.max()
    nodes = nodes - 1  # make vertices numbered from zero
    adj = np.zeros((num_v, num_v))  # adjacency matrix
    for node in nodes:
        adj[node[0], node[1]] = 1

    # count motifs
    if n > num_v:
        print('Error: motif has more vertices than input graph')
        return

    motifs = q1(n, to_file=False)
    subgraphs = get_subgraphs(adj, n)
    data = 'n=' + str(len(motifs)) + '\n'
    for idx, motif in enumerate(motifs):
        data += '#' + str(idx+1) + '\n'
        data += 'count=' + str(count_motifs(motif, subgraphs)) + '\n'

    f = open('q2_output.txt', 'w')
    data = f.write(data)
    f.close()


# **** MAIN ****

# print('********** q1 **********')
print('G(|V|=1) Count: ', len(q1(1)))
print('G(|V|=2) Count: ', len(q1(2)))
print('G(|V|=3) Count: ', len(q1(3)))
print('G(|V|=4) Count: ', len(q1(4)))
print('For n=5 takes more than 1 hour')

print('********** q2 **********')
motif_size = 3
q2('q2_input.txt', motif_size)
print('q2_output.txt successfully saved')
