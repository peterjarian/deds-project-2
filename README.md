# Q-Learning Grid Game

## Introduction
This project implements a grid-based game where an AI agent learns to navigate through a maze using Q-learning, a reinforcement learning algorithm. The agent must find the optimal path to reach a reward while avoiding walls and dangers.

Key features:
- Grid-based environment with walls, dangers, and rewards
- Q-learning implementation for AI training
- Real-time visualization of the agent's learning process
- Manual and automatic training modes
- Episode tracking and performance metrics

## Installation

### Prerequisites
- Python 3.8 or higher
- Poetry (Python dependency management)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/peterjarian/deds-project-2.git
cd deds-project-2
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Run the game:
```bash
poetry run python src/main.py
```

### Controls
- **R**: Reset the game
- **M**: Toggle between manual and training mode
- **Arrow keys** or **WASD**: Move the agent (in manual mode)
