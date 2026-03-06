import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# PARAMETERS
n = 5
dt = 0.03
scenario = 5   # 1–5


positions = 6*np.random.uniform(-60,60,(n,2))
errors = []


# GRAPH DEFINITIONS

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


def compute_laplacian(A):
    D = np.diag(np.sum(A,axis=1))
    return D - A


# SCENARIO SELECTION

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
    title = "Malicious Agent"


L = compute_laplacian(A)


# EIGENVALUES

eigvals = np.sort(np.real(np.linalg.eigvals(L)))


# FIGURE WITH 3 PANELS

fig, axs = plt.subplots(1,3,figsize=(16,5))


# PANEL 1 — AGENTS

ax = axs[0]
ax.set_title("Agent Dynamics")
ax.grid(True)

scat = ax.scatter(positions[:,0],positions[:,1],s=120)

lines = []


# PANEL 2 — EIGENVALUES

ax2 = axs[1]

ax2.scatter(range(len(eigvals)),eigvals)

ax2.set_title("Laplacian Eigenvalues")

ax2.set_xlabel("Index")
ax2.set_ylabel("Eigenvalue")

ax2.grid(True)


# PANEL 3 — ERROR

ax3 = axs[2]

line_error, = ax3.plot([],[])

ax3.set_title("Consensus Error")

ax3.set_xlabel("Time")
ax3.set_ylabel("Error")

ax3.set_yscale("log")

ax3.grid(True)


# DRAW GRAPH EDGES

def draw_edges():

    global lines

    for line in lines:
        line.remove()

    lines=[]

    for i in range(n):
        for j in range(i+1,n):

            if A[i,j]==1:

                line,=ax.plot(
                    [positions[i,0],positions[j,0]],
                    [positions[i,1],positions[j,1]],
                    color='gray',
                    alpha=0.3
                )

                lines.append(line)


draw_edges()


# UPDATE FUNCTION

def update(frame):

    global positions

    dx = -L @ positions


    if scenario == 4:
        dx += 0.8*np.random.randn(n,2)


    if scenario == 5:
        dx[0] = 0


    positions += dt*dx

    scat.set_offsets(positions)

    draw_edges()


    # AUTO SCALE AGENT AXIS

    ax.set_xlim(np.min(positions[:,0])-20, np.max(positions[:,0])+20)
    ax.set_ylim(np.min(positions[:,1])-20, np.max(positions[:,1])+20)


    # CONSENSUS ERROR

    mean_pos = np.mean(positions,axis=0)

    error = np.linalg.norm(positions-mean_pos) + 1e-6

    errors.append(error)


    line_error.set_data(range(len(errors)),errors)

    ax3.set_xlim(0,len(errors))
    ax3.set_ylim(min(errors)*0.9,max(errors)*1.1)


    # MALICIOUS COLOR

    if scenario == 5:

        colors = ['red'] + ['blue']*(n-1)
        scat.set_color(colors)


    return scat,line_error,*lines


ani = FuncAnimation(fig,update,frames=500,interval=500)

plt.suptitle(title)

plt.tight_layout()

plt.show()