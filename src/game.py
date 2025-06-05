from level import CelType, Level
from player import Player
from qlearner import QLearner


class GameModesType:
    MANUAL = 0
    TRAINING = 1


class InputType:
    MOVE_UP = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    TOGGLE_MODE = 4


class Game:
    def __init__(self, grid_size: int):
        self.level = Level(grid_size)
        self.player = Player(self)
        self.mode = GameModesType.TRAINING
        # Initialize Q-learner with hyperparameters
        self.q_learner = QLearner(
            learning_rate=0.2, discount_rate=0.9, exploration_rate=0.3, grid_size=self.level.grid.shape[0]
        )
        # Episode tracking
        self.episode_steps = 0
        self.episode_reward = 0
        self.episode_count = 0

    def handle_input(self, input: int) -> tuple[tuple[int, int], bool]:
        current_position = self.player.get_position()
        y, x = self.__calculate_requested_position(input)
        next_position = (y, x)

        # Check for out of bounds
        if y < 0 or x < 0 or y >= len(self.level.grid) or x >= len(self.level.grid):
            if self.mode == GameModesType.TRAINING:
                # Update Q-table with negative reward for hitting wall
                self.q_learner.update_q_table(current_position, input, -5, current_position)
                self.episode_reward += -5
            return self.player.get_position(), False

        # Check for walls
        if self.level.grid[y, x] == CelType.WALL:
            if self.mode == GameModesType.TRAINING:
                # Update Q-table with negative value for hitting wall
                self.q_learner.update_q_table(current_position, input, -5, current_position)
                self.episode_reward += -5
            return self.player.get_position(), False

        # Check for dangers
        if self.level.grid[y, x] == CelType.DANGER:
            if self.mode == GameModesType.TRAINING:
                # Update Q-table with negative value for hitting danger
                self.q_learner.update_q_table(current_position, input, -20, next_position)
                self.episode_reward += -20
                print(
                    f"Episode {self.episode_count}: DEAD, steps={self.episode_steps}, total_reward={self.episode_reward}"
                )
                self.episode_count += 1
                self.episode_steps = 0
                self.episode_reward = 0
            self.player.add_death()
            self.player.reset_position()
            return self.player.get_position(), True

        # Check for reward
        if self.level.grid[y, x] == CelType.REWARD:
            if self.mode == GameModesType.TRAINING:
                # Update Q-table with positive value for reward
                self.q_learner.update_q_table(current_position, input, 200, next_position)
                self.episode_reward += 200
                print(
                    f"Episode {self.episode_count}: SUCCESS, steps={self.episode_steps}, total_reward={self.episode_reward}"
                )
                self.episode_count += 1
                self.episode_steps = 0
                self.episode_reward = 0
            self.player.add_success()
            self.player.reset_position()
            return self.player.get_position(), True

        if self.mode == GameModesType.TRAINING:
            if next_position == current_position:
                self.q_learner.update_q_table(current_position, input, -5, next_position)
                self.episode_reward += -5
            elif self.player.has_visited(next_position):
                # Extra penalty for revisiting a location
                self.q_learner.update_q_table(current_position, input, -5, next_position)
                self.episode_reward += -5
            else:
                # Normal move penalty
                self.episode_reward += -2

        self.episode_steps += 1
        self.player.move(next_position)
        return self.player.get_position(), False

    def reset(self):
        self.level = Level(self.level.size)
        self.player.reset_position()
        self.player.deaths = 0
        self.player.successes = 0
        # Reset episode tracking
        self.episode_steps = 0
        self.episode_reward = 0
        self.episode_count = 0

    def __calculate_requested_position(self, input: int) -> tuple[int, int]:
        y, x = self.player.get_position()

        if input == InputType.MOVE_UP:
            return (y - 1, x)
        elif input == InputType.MOVE_LEFT:
            return (y, x - 1)
        elif input == InputType.MOVE_RIGHT:
            return (y, x + 1)
        elif input == InputType.MOVE_DOWN:
            return (y + 1, x)
        else:
            raise TypeError("Unknown input")

    def auto_move(self):
        current_position = self.player.get_position()
        action = self.q_learner.get_action(current_position)
        self.handle_input(action)
