import numpy as np


class QLearner:
    def __init__(self, learning_rate: float, discount_rate: float, exploration_rate: float, grid_size: int):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros((grid_size, grid_size, 4))

    def update_q_table(
        self, current_position: tuple[int, int], action: int, reward: int, next_position: tuple[int, int]
    ):
        current_q = self.q_table[current_position[0], current_position[1], action]
        next_max_q = np.max(self.q_table[next_position[0], next_position[1]])
        self.q_table[current_position[0], current_position[1], action] = current_q + self.learning_rate * (
            reward + self.discount_rate * next_max_q - current_q
        )

    def get_action(self, state: tuple[int, int]) -> int:

        if np.random.random() < self.exploration_rate:
            # Exploration: choose random action
            return np.random.randint(4)
        else:
            # Exploitation: choose best action
            return self.get_best_action(state)

    def get_best_action(self, state: tuple[int, int]) -> int:
        return int(np.argmax(self.q_table[state[0], state[1]]))
