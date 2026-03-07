import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import requests
requests.post("http://10.72.241.56:5000/start")


"""
Guess the malicious agents: They move towards the centroid of the polygon formed by them.
They also tend to form their own independent cluster during simulation but eventually other agents also converge to the same cluster
"""

n = 20
num_malicious = 4
dt = 0.001
frames = 250
show_edges = True
reveal_frame = 220
mal_mov_fac = 5


def random_graph(n, p=0.4):
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.rand() < p:
                A[i, j] = 1
                A[j, i] = 1
    return A


def compute_laplacian(A):
    D = np.diag(np.sum(A, axis=1))
    return D - A


A = random_graph(n, p=0.5)
L = compute_laplacian(A)

malicious_agents = np.random.choice(n, num_malicious, replace=False)
print("Teacher answer: malicious agents =", malicious_agents)

positions = 40 * np.random.uniform(-1, 1, (n, 2))


fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Puzzle: Identify the Malicious Agents")
ax.grid(True)


# Create circle nodes
circles = []
labels = []

radius = 1.0

for i in range(n):

    circle = Circle(
        (positions[i,0], positions[i,1]),
        radius,
        color="blue",
        zorder=2
    )

    ax.add_patch(circle)
    circles.append(circle)

    label = ax.text(
        positions[i,0],
        positions[i,1],
        str(i),
        color="white",
        ha="center",
        va="center",
        fontsize=10,
        weight="bold",
        zorder=3
    )

    labels.append(label)


lines = []
median_lines = []
revealed = False


def draw_edges():
    global lines

    for line in lines:
        line.remove()

    lines = []

    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] == 1:
                line, = ax.plot(
                    [positions[i,0], positions[j,0]],
                    [positions[i,1], positions[j,1]],
                    color="gray",
                    alpha=0.3,
                    zorder=1
                )

                lines.append(line)


def draw_medians():
    global median_lines

    for line in median_lines:
        line.remove()

    median_lines = []

    mal_pos = positions[malicious_agents]

    for i, agent in enumerate(malicious_agents):

        other = np.delete(mal_pos, i, axis=0)
        midpoint = np.mean(other, axis=0)

        p = positions[agent]

        line, = ax.plot(
            [p[0], midpoint[0]],
            [p[1], midpoint[1]],
            linestyle=":",
            color="red",
            linewidth=2
        )

        median_lines.append(line)


if show_edges:
    draw_edges()


def update(frame):
    global positions, revealed

    dx = -L @ positions

    mal_pos = positions[malicious_agents]
    centroid = np.mean(mal_pos, axis=0)

    for agent in malicious_agents:
        direction = (centroid - positions[agent]) * mal_mov_fac
        dx[agent] = direction

    positions += dt * dx


    for i in range(n):

        circles[i].center = positions[i]

        labels[i].set_position(positions[i])


    if frame >= reveal_frame and not revealed:

        for idx in malicious_agents:
            circles[idx].set_color("red")

        revealed = True


    if show_edges:
        draw_edges()

    if revealed:
        draw_medians()

    min_pos = min(np.min(positions[:,0]), np.min(positions[:,1]))
    max_pos = max(np.max(positions[:,0]), np.max(positions[:,1]))
    ax.set_xlim(min_pos - 10, max_pos + 10)
    ax.set_ylim(min_pos - 10, max_pos + 10)

    return *circles, *labels, *lines, *median_lines


ani = FuncAnimation(fig, update, frames=frames, interval=100)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.tight_layout()
plt.show()