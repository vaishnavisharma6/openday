import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class ConsensusSimulation:

    def __init__(self, n_agents=20, scenario="random_attack"):

        self.n = n_agents
        self.alpha = 0.05
        self.scenario = scenario

        # initial agent positions
        self.positions = np.random.uniform(-50, 50, (self.n, 2))

        # adjacency matrix (fully connected)
        self.A = np.ones((self.n, self.n)) - np.eye(self.n)

        self.L = self.compute_laplacian(self.A)

        # create two plots
        self.fig, (self.ax, self.ax_eig) = plt.subplots(1, 2, figsize=(14, 7))

        # robot space
        self.ax.set_xlim(-70, 70)
        self.ax.set_ylim(-70, 70)
        self.ax.set_title(f"Swarm Behavior: {scenario}")

        # eigenvalue plot
        self.ax_eig.set_title("Laplacian Eigenvalues")
        self.ax_eig.set_xlabel("Index")
        self.ax_eig.set_ylabel("Eigenvalue")

        # scatter for robots
        self.scat = self.ax.scatter(
            self.positions[:, 0],
            self.positions[:, 1],
            marker='x',
            s=200
        )

        # compute eigenvalues
        self.eigvals = self.compute_eigenvalues()

        self.eig_plot = self.ax_eig.scatter(
            range(len(self.eigvals)),
            self.eigvals,
            s=80
        )

        self.ax_eig.axhline(0, color='black')

        # label λ2
        self.lambda_text = self.ax_eig.text(
            0.5,
            0.9,
            "",
            transform=self.ax_eig.transAxes,
            fontsize=14,
            ha="center"
        )

        self.lines = []

        self.draw_edges()

    def compute_laplacian(self, A):

        D = np.diag(np.sum(A, axis=1))
        return D - A

    def compute_eigenvalues(self):

        eigvals = np.linalg.eigvals(self.L)
        eigvals = np.sort(np.real(eigvals))

        return eigvals

    def draw_edges(self):

        for line in self.lines:
            line.remove()

        self.lines = []

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.A[i, j] == 1:

                    line, = self.ax.plot(
                        [self.positions[i, 0], self.positions[j, 0]],
                        [self.positions[i, 1], self.positions[j, 1]],
                        color="gray",
                        alpha=0.15
                    )

                    self.lines.append(line)

    def consensus_step(self):

        dx = -self.L @ self.positions
        self.positions += self.alpha * dx

    def malicious_behavior(self, frame):

        # agent 0 is malicious

        if self.scenario == "circle_attack":

            self.positions[0, 0] = 40 * np.cos(frame * 0.05)
            self.positions[0, 1] = 40 * np.sin(frame * 0.05)

        elif self.scenario == "random_attack":

            self.positions[0] += np.random.randn(2) * 5

        elif self.scenario == "drift_attack":

            self.positions[0] += np.array([0.5, 0.3])

        elif self.scenario == "repulsion_attack":

            for i in range(1, self.n):
                direction = self.positions[i] - self.positions[0]
                self.positions[i] += 0.03 * direction

        elif self.scenario == "fake_position":

            fake = self.positions[0] + np.array([40, 40])

            for i in range(1, self.n):
                direction = fake - self.positions[i]
                self.positions[i] += 0.03 * direction

    def update(self, frame):

        # normal consensus
        self.consensus_step()

        # malicious behavior
        self.malicious_behavior(frame)

        # update positions
        self.scat.set_offsets(self.positions)

        colors = ["red"] + ["blue"] * (self.n - 1)
        self.scat.set_color(colors)

        self.draw_edges()

        # update eigenvalues
        self.eigvals = self.compute_eigenvalues()

        self.eig_plot.set_offsets(
            np.column_stack((range(len(self.eigvals)), self.eigvals))
        )

        self.lambda_text.set_text(f"λ₂ = {self.eigvals[1]:.3f}")

        return self.scat, *self.lines, self.eig_plot

    def run(self):

        self.ani = FuncAnimation(
            self.fig,
            self.update,
            frames=1000,
            interval=2000
        )

        plt.show()


# -----------------------------
# Choose scenario
# -----------------------------

sim = ConsensusSimulation(
    n_agents=5,
    scenario="repulsion_attack"
)

sim.run()