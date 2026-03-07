import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import graphs as g


n = 6
dt = 0.02
frames = 200
show_edges = True



def compute_laplacian(A):
    D = np.diag(np.sum(A, axis=1))
    return D - A


A = g.convex_polygon_graph(n)
L = compute_laplacian(A)

true_edges = int(np.sum(A) // 2)
print("Teacher answer: number of edges =", true_edges)


positions = 40 * np.random.uniform(-1, 1, (n, 2))


fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Guess the Number of Edges from Motion")
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

plt.tight_layout()
plt.show()