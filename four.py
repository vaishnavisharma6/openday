import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

# Initial states
x0 = np.array([10, 25, 60, 80, 95])
n = len(x0)
t_span = np.linspace(0, 5, 200)

def get_consensus_path(strength):
    # Create a Ring Laplacian scaled by 'strength'
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i+1)%n] = A[(i+1)%n, i] = strength
    L = np.diag(np.sum(A, axis=1)) - A
    
    # Calculate convergence
    states = np.array([expm(-L * t) @ x0 for t in t_span])
    return states, np.sort(np.linalg.eigvals(L).real)[1]

# Compare three different Eigenvalue "Speeds"
strengths = [0.2, 1.0, 5.0]
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

for i, s in enumerate(strengths):
    data, l2 = get_consensus_path(s)
    axes[i].plot(t_span, data)
    axes[i].set_title(f"Strength: {s} | $\lambda_2$: {l2:.2f}")
    axes[i].grid(True, alpha=0.3)
    axes[i].set_xlabel("Time")

axes[0].set_ylabel("Agent Opinions")
plt.tight_layout()
plt.show()