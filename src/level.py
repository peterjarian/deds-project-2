import random
import numpy as np


class CelType:
    AIR = 0
    WALL = 1
    DANGER = 2
    REWARD = 3
    SPAWN = 4


class Level:
    def __init__(self, size: int):
        self.__obstacle_percentage = 0.30
        self.size = size
        self.reward_position = (0, 0)
        self.spawn_position = (0, 0)
        self.grid = np.zeros((size, size), dtype=int)

        if size < 5 or size > 12:
            raise ValueError("Size must be between 5 and 12")

        self.__create_grid()

    def get_grid(self):
        return self.grid

    def __create_grid(self):
        # Choose a random corner for the reward position
        corners = [(0, 0), (0, self.size - 1), (self.size - 1, 0), (self.size - 1, self.size - 1)]
        reward_position = corners[random.randint(0, 3)]
        self.reward_position = reward_position
        self.grid[reward_position] = CelType.REWARD

        # Choose the opposite corner of the reward for the spawn position
        spawn_position = (self.size - 1 - reward_position[0], self.size - 1 - reward_position[1])
        self.spawn_position = spawn_position

        # Get the total number of obstacles for the grid size
        # We want to ensure that 80% of the total obstacles are walls
        # The remaining cells become dangers
        total_obstacles = self.__get_total_obstacles()
        total_wall_cells = round(total_obstacles / 100 * 80)
        total_danger_cells = round(total_obstacles - total_wall_cells)

        # On a small grid, we sometimes don't have enough space to place obstacles
        # Adding a maximum number of attempts prevents an infinite loop
        max_attempts = 100

        # Place all walls
        wall_cells_placed = 0
        attempts = 0

        while wall_cells_placed < total_wall_cells and attempts < max_attempts:
            position = self.__get_random_grid_position()
            # Don't place walls on spawn or reward
            if self.grid[position] == CelType.AIR and position != self.spawn_position:
                self.grid[position] = CelType.WALL
                if self.__resolvable():
                    wall_cells_placed += 1
                else:
                    self.grid[position] = CelType.AIR
            attempts += 1

        # Place all dangers
        danger_cells_placed = 0
        attempts = 0

        while danger_cells_placed < total_danger_cells and attempts < max_attempts:
            position = self.__get_random_grid_position()
            # Don't place dangers on spawn or reward
            if self.grid[position] == CelType.AIR and position != self.spawn_position:
                self.grid[position] = CelType.DANGER
                if self.__resolvable():
                    danger_cells_placed += 1
                else:
                    self.grid[position] = CelType.AIR
            attempts += 1

    def __get_total_obstacles(self):
        total = self.size * self.size
        return round(total * self.__obstacle_percentage)

    def __get_random_grid_position(self) -> tuple[int, int]:
        y = random.randint(0, self.size - 1)
        x = random.randint(0, self.size - 1)
        return (y, x)  # Return as (y,x) for numpy consistency

    def __resolvable(self) -> bool:
        # Make a copy
        grid_copy = np.copy(self.grid)
        visited = set()  # Keep track of visited positions
        queue = [self.spawn_position]  # Start from spawn
        visited.add(self.spawn_position)

        while queue:
            position = queue.pop(0)  # Get the first position from the queue

            # If we've reached the reward, the path is valid
            if position == self.reward_position:
                return True

            # Check all 4 directions
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_y = position[0] + dy
                new_x = position[1] + dx
                new_pos = (new_y, new_x)

                # Check if the new position is valid and not visited
                if (
                    0 <= new_y < self.size
                    and 0 <= new_x < self.size
                    and new_pos not in visited
                    and grid_copy[new_y, new_x] != CelType.WALL
                    and grid_copy[new_y, new_x] != CelType.DANGER
                ):
                    queue.append(new_pos)
                    visited.add(new_pos)

        return False
