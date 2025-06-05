from level import CelType
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from game import Game


class Player:
    def __init__(self, game: "Game"):
        self.game = game
        self.deaths = 0
        self.successes = 0
        self.position = game.level.spawn_position
        self.visited_positions: Set[tuple[int, int]] = {self.position}

    def move(self, new_position: tuple[int, int]):
        self.position = new_position
        self.visited_positions.add(new_position)

    def reset_position(self):
        self.position = self.game.level.spawn_position
        self.visited_positions = {self.game.level.spawn_position}

    def add_success(self):
        self.successes += 1

    def add_death(self):
        self.deaths += 1

    def get_position(self):
        return self.position

    def has_visited(self, position: tuple[int, int]) -> bool:
        return position in self.visited_positions
