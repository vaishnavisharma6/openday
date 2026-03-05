import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

def get_laplacian_complete(n):
    # Every node connected to every other node
    adj = np.ones((n, n)) - np.eye(n)
    deg = np.diag(np.sum(adj, axis=1))
    return deg - adj

def get_laplacian_path(n):
    # Nodes connected in a single line (1-2-3-4...)
    adj = np.zeros((n, n))
    for i in range(n-1):
        adj[i, i+1] = adj[i+1, i] = 1
    deg = np.diag(np.sum(adj, axis=1))
    return deg - adj

# Parameters
n_agents = 6
t_span = np.linspace(0, 5, 100)
x0 = np.array([10, 25, 40, 55, 70, 85]) # Initial opinions

# 1. Complete Graph (High Algebraic Connectivity)
L_comp = get_laplacian_complete(n_agents)
eig_comp = np.sort(np.linalg.eigvals(L_comp))
# lambda_2 for complete graph is n_agents

# 2. Path Graph (Low Algebraic Connectivity)
L_path = get_laplacian_path(n_agents)
eig_path = np.sort(np.linalg.eigvals(L_path))
# lambda_2 for path graph is 2*(1 - cos(pi/n))

# Simulation
x_comp = np.array([expm(-L_comp * t) @ x0 for t in t_span])
x_path = np.array([expm(-L_path * t) @ x0 for t in t_span])

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(t_span, x_comp)
ax1.set_title(f"Complete Graph (High $\lambda_2$ = {eig_comp[1]:.2f})\nBehavior: Instant Agreement")
ax1.set_xlabel("Time")
ax1.set_ylabel("Agent State")
ax1.grid(True)

ax2.plot(t_span, x_path)
ax2.set_title(f"Path Graph (Low $\lambda_2$ = {eig_path[1]:.2f})\nBehavior: Sluggish Diffusion")
ax2.set_xlabel("Time")
ax2.grid(True)

plt.tight_layout()
plt.show()