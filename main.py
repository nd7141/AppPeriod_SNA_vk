from __future__ import division
import networkx as nx
import time
import numpy as np
from scipy.sparse import *

if __name__ == "__main__":

    start = time.time()
    # G = nx.Graph()
    # with open("output.txt") as f:
    #     for i, line in enumerate(f):
    #         if i  == 5000000:
    #             print i, time.time() - start
    #             break
    #         data = line.split()
    #         try:
    #             u, v = map(int, data)
    #             G.add_edge(u, v)
    #         except:
    #             continue
    A = lil_matrix((9839435,9839435), dtype=np.int32)
    print time.time() - start
    node_idx = 0
    id2node = dict()
    with open("output.txt") as f:
        for i, line in enumerate(f):
            if i == 10000000:
                break
            id1, id2 = map(int, line.split()) # row, column
            if id1 not in id2node:
                id2node[id1] = node_idx
                node_idx += 1
            if id2 not in id2node:
                id2node[id2] = node_idx
                node_idx += 1
            node1 = id2node[id1]
            node2 = id2node[id2]
            A[node1,node2] = 1
            A[node2,node1] = 1
            
    print 'Read graph in %s' %(time.time() - start)

    console = []

