import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def compute_laplacian(A):
    D = np.diag(np.sum(A, axis=1))
    return D - A

def simulate_consensus(L, x0, dt=0.05, steps=400, noise=None):
    x = x0.copy()
    history = [x.copy()]
    
    for _ in range(steps):
        if noise is None:
            dx = -L @ x
        else:
            dx = -L @ x + noise(x.shape)
        x = x + dt * dx
        history.append(x.copy())
        
    return np.array(history)


n = 15
A = np.ones((n, n)) - np.eye(n)   # fully connected
L = compute_laplacian(A)

x0 = np.random.randn(n)
history = simulate_consensus(L, x0)

plt.plot(history)
plt.title("Fully Connected Graph - Fast Consensus")
plt.show()


n = 15
A = np.zeros((n, n))

for i in range(n-1):
    A[i, i+1] = 1
    A[i+1, i] = 1

L = compute_laplacian(A)

x0 = np.random.randn(n)
history = simulate_consensus(L, x0)

plt.plot(history)
plt.title("Sparse Chain Graph - Slow Consensus")
plt.show()