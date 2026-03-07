import numpy as np

def convex_polygon_graph(n):
    """
    Create a convex polygon (cycle) graph with n nodes.
    Each node connects to its two neighbors.
    """

    A = np.zeros((n, n))

    for i in range(n):
        j = (i + 1) % n
        A[i, j] = 1
        A[j, i] = 1

    return A

def random_graph(n, sparsity_percent):
    """
    Return adjacency matrix of a sparse graph
    """

    A = np.zeros((n, n))

    total_possible_edges = n * (n - 1) // 2
    num_edges = int((sparsity_percent / 100) * total_possible_edges)

    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))

    chosen_edges = np.random.choice(len(edges), num_edges, replace=False)

    for idx in chosen_edges:
        i, j = edges[idx]
        A[i, j] = 1
        A[j, i] = 1

    return A


def fully_connected(n):
    return np.ones((n,n)) - np.eye(n)

def chain_graph(n):
    A = np.zeros((n,n))
    for i in range(n-1):
        A[i,i+1] = 1
        A[i+1,i] = 1
    return A

def disconnected_graph(n):
    A = np.zeros((n,n))

    for i in range(n//2 - 1):
        A[i,i+1] = 1
        A[i+1,i] = 1

    for i in range(n//2,n-1):
        A[i,i+1] = 1
        A[i+1,i] = 1

    return A

def custom_graph():
    A = [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ]
    return np.array(A, dtype= np.float32)