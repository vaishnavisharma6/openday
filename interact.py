import numpy as np


def polygon_with_center(n, radius=20):
    """
    Create positions where one node is at the center and the remaining
    nodes are placed symmetrically on a circle.

    n : total number of nodes
    radius : radius of the polygon

    Returns
    -------
    positions : (n,2) array of coordinates
    """

    positions = np.zeros((n, 2))

    num_outer = n - 1
    angles = np.linspace(0, 2*np.pi, num_outer, endpoint=False)

    for i, angle in enumerate(angles):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        positions[i+1] = [x, y]

    return positions

def random_positions(n, x_range=(-60, 60), y_range=(-60, 60)):
    positions = 6*np.random.uniform(x_range[0], x_range[1], (n, 2))
    positions[:, 1] = 6*np.random.uniform(y_range[0], y_range[1], n)
    return positions


def custom_positions():
    positions = np.array(
        [
            [0.0, 0.0], [10.0, 10.0], [10.0, -10.0], [-10.0, -10.0], [-10.0, 10.0]
        ]
    ) * 5.0
    return positions