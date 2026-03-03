import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# PARAMETERS

n = 15
dt = 0.03
scenario = 5   # Change 1–5

positions =  6*  np.random.uniform(-60, 60, (n, 2))


# GRAPH DEFINITIONS


def fully_connected(n):
    return np.ones((n, n)) - np.eye(n)

def chain_graph(n):
    A = np.zeros((n, n))
    for i in range(n-1):
        A[i, i+1] = 1
        A[i+1, i] = 1
    return A

def disconnected_graph(n):
    A = np.zeros((n, n))
    for i in range(n//2 - 1):
        A[i, i+1] = 1
        A[i+1, i] = 1
    for i in range(n//2, n-1):
        A[i, i+1] = 1
        A[i+1, i] = 1
    return A

def compute_laplacian(A):
    D = np.diag(np.sum(A, axis=1))
    return D - A


# SCENARIO


if scenario == 1:
    A = fully_connected(n)
    title = "Fully Connected Graph"
elif scenario == 2:
    A = chain_graph(n)
    title = "Sparse Chain Graph"
elif scenario == 3:
    A = disconnected_graph(n)
    title = "Disconnected Graph"
elif scenario == 4:
    A = fully_connected(n)
    title = "Consensus with Noise"
elif scenario == 5:
    A = fully_connected(n)
    title = "Malicious Agent (Red)"

L = compute_laplacian(A)


# PLOT


fig, ax = plt.subplots(figsize=(10,10))
ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
ax.set_title(title)
ax.grid(True)

scat = ax.scatter(positions[:,0], positions[:,1], s=120, marker = 'x')

lines = []

def draw_edges():
    global lines
    # Remove old edges
    for line in lines:
        line.remove()
    lines = []

    # Draw new edges
    for i in range(n):
        for j in range(i+1, n):
            if A[i,j] == 1:
                line, = ax.plot([positions[i,0], positions[j,0]],
                                [positions[i,1], positions[j,1]],
                                color='gray', alpha=0.3)
                lines.append(line)

draw_edges()


# UPDATE


def update(frame):
    global positions

    dx = -L @ positions

    if scenario == 4:
        dx += 0.8 * np.random.randn(n, 2)

    if scenario == 5:
        dx[0] = 0

    positions += dt * dx

    scat.set_offsets(positions)

    if scenario == 5:
        colors = ['red'] + ['blue']*(n-1)
        scat.set_color(colors)

    draw_edges()

    return scat, *lines

ani = FuncAnimation(fig, update, frames=800, interval=3000)
plt.show()