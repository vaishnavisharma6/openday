# Multi-Agent Consensus Interactive Demo

This project demonstrates consensus dynamics in multi-agent systems using graph-based interactions. The repository includes interactive simulations and gamified experiments designed to help students intuitively understand concepts such as consensus, graph connectivity, and adversarial agents.

The project was created as a science demonstration tool where participants observe the motion of agents and answer questions based on system behavior.

## Features

* Simulation of consensus dynamics using graph Laplacian.
* Random, chain, disconnected, and custom graph structures.
* Visualization of agent motion and communication edges.
* Experiments involving malicious agents that deviate from consensus rules.
* Interactive web interface for collecting student responses.
* Real-time voting for identifying clusters or malicious agents.
* Gamified setup suitable for classroom or science exhibition demonstrations.

## Experiments

### Consensus Behavior

Agents follow a simple local rule where each agent moves toward the average position of its neighbors. Over time, this leads to global agreement among agents if the graph is connected.

### Cluster Identification Game

Participants observe the movement of agents and attempt to determine how many disconnected clusters exist in the system.

### Malicious Agent Detection

Some agents intentionally deviate from the consensus law and instead move toward the centroid of the group formed by other malicious agents. Participants must identify which nodes behave maliciously.

## Visualization

Agents are visualized as moving circles labeled with node indices. Edges represent communication links. In some experiments edges are hidden to make the problem more challenging.

Malicious agents can be revealed after the experiment for verification.

## Voting System

A lightweight Flask and SocketIO server provides a voting interface for participants:

* Up to 20 selectable nodes arranged in a grid
* Maximum of four selections allowed
* Responses locked after submission
* Simulation start notification sent to all participants
* Response times recorded automatically

## Requirements

Python 3.8+

Required Python packages:

```
numpy
matplotlib
flask
flask-socketio
requests
```

Install dependencies:

```
pip install numpy matplotlib flask flask-socketio requests
```

## Running the Simulation

Start the voting server:

```
python server.py
```

Participants can access the interface from their phones using:

```
http://<server-ip>:5000
```

Run the simulation script:

```
python malicious_agents_simulation.py
```

The simulation will automatically notify the server when it begins.

## Educational Goals

This project is designed to illustrate several concepts:

* Distributed coordination
* Graph-based communication
* Emergent collective behavior
* Fault detection in multi-agent systems
* The role of network topology in system dynamics

The interactive format encourages students to observe patterns, make predictions, and verify their hypotheses.


