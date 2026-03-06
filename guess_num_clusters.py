import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests
requests.post("http://10.72.241.56:5000/start")


n = np.random.randint(30, 50)
m = np.random.randint(3, 7)
dt = 0.001
frames = 200
show_edges = True


def disconnected_clusters_graph(n, m):
    A = np.zeros((n, n))
    cluster_size = n // m

    clusters = []
    start = 0
    for i in range(m):
        if i == m - 1:
            end = n
        else:
            end = start + cluster_size
        clusters.append(list(range(start, end)))
        start = end

    for cluster in clusters:
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                u = cluster[i]
                v = cluster[j]
                A[u, v] = 1
                A[v, u] = 1

    return A


def compute_laplacian(A):
    D = np.diag(np.sum(A, axis=1))
    return D - A


A = disconnected_clusters_graph(n, m)
L = compute_laplacian(A)




positions = 40 * np.random.uniform(-1, 1, (n, 2))


fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Guess the Number of Clusters from Motion")
ax.grid(True)

scat = ax.scatter(positions[:, 0], positions[:, 1], s=120)

lines = []


def draw_edges():
    global lines

    for line in lines:
        line.remove()

    lines = []

    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] == 1:
                line, = ax.plot(
                    [positions[i, 0], positions[j, 0]],
                    [positions[i, 1], positions[j, 1]],
                    color="gray",
                    alpha=0.4
                )
                lines.append(line)


if show_edges:
    draw_edges()


def update(frame):
    global positions

    dx = -L @ positions
    positions += dt * dx

    scat.set_offsets(positions)

    if show_edges:
        draw_edges()

    ax.set_xlim(np.min(positions[:, 0]) - 10, np.max(positions[:, 0]) + 10)
    ax.set_ylim(np.min(positions[:, 1]) - 10, np.max(positions[:, 1]) + 10)

    return scat, *lines


ani = FuncAnimation(fig, update, frames=frames, interval=100)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.tight_layout()
plt.show()

print("Teacher answer: number of clusters =", m)