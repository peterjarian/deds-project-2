import pygame
from game import Game, GameModesType
from level import CelType

CELL_SIZE = 60
FONT_SIZE = 24
STATS_PANEL_HEIGHT = 80

HEX_COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GRAY": (128, 128, 128),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "DARK_GRAY": (40, 40, 40),
}

COLOR_MAPPINGS = {
    "BACKGROUND": HEX_COLORS["BLACK"],
    "STATS_PANEL": HEX_COLORS["DARK_GRAY"],
    "GRID_LINES": HEX_COLORS["BLACK"],
    "DEATHS_TEXT": HEX_COLORS["RED"],
    "SUCCESSES_TEXT": HEX_COLORS["GREEN"],
    "MODE_TEXT": HEX_COLORS["WHITE"],
    "AIR": HEX_COLORS["WHITE"],
    "WALL": HEX_COLORS["GRAY"],
    "DANGER": HEX_COLORS["RED"],
    "REWARD": HEX_COLORS["GREEN"],
    "PLAYER": HEX_COLORS["BLUE"],
}

MODE_TEXT = {GameModesType.MANUAL: "Manual", GameModesType.TRAINING: "Training"}


class Renderer:
    def __init__(self, screen: pygame.Surface, game: Game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.window_size = CELL_SIZE * game.level.size

    def draw(self):
        self.__draw_stats_panel()
        self.__draw_grid()
        self.__draw_player()

        # Update the screen
        pygame.display.flip()

    def __draw_stats_panel(self):
        # Background
        stats_panel = pygame.Rect(0, 0, self.window_size, STATS_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_MAPPINGS["STATS_PANEL"], stats_panel)

        # Text
        deaths_text = self.font.render(str(self.game.player.deaths), True, COLOR_MAPPINGS["DEATHS_TEXT"])
        successes_text = self.font.render(str(self.game.player.successes), True, COLOR_MAPPINGS["SUCCESSES_TEXT"])
        mode_text = self.font.render(MODE_TEXT[self.game.mode], True, COLOR_MAPPINGS["MODE_TEXT"])

        # Center
        deaths_position = deaths_text.get_rect(center=(self.window_size // 4, STATS_PANEL_HEIGHT // 2))
        successes_position = successes_text.get_rect(center=(3 * self.window_size // 4, STATS_PANEL_HEIGHT // 2))
        mode_position = mode_text.get_rect(center=(self.window_size // 2, STATS_PANEL_HEIGHT // 2))

        # Place the text on the screen
        self.screen.blit(deaths_text, deaths_position)
        self.screen.blit(successes_text, successes_position)
        self.screen.blit(mode_text, mode_position)

    def __draw_grid(self):
        grid = self.game.level.get_grid()
        grid_size = self.game.level.size

        # Loop through the entire grid
        for y in range(grid_size):
            for x in range(grid_size):
                # Check cell type
                cell_value = grid[y, x]

                # Calculate where the cell should be drawn on the screen
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    y * CELL_SIZE + STATS_PANEL_HEIGHT,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                # Convert all cell types to a color
                cell_type = {
                    CelType.AIR: "AIR",
                    CelType.WALL: "WALL",
                    CelType.DANGER: "DANGER",
                    CelType.REWARD: "REWARD",
                }[cell_value]

                pygame.draw.rect(self.screen, COLOR_MAPPINGS[cell_type], rect)
                pygame.draw.rect(self.screen, COLOR_MAPPINGS["GRID_LINES"], rect, 1)

    def __draw_player(self):
        player_pos = self.game.player.get_position()

        # Ensure the player is centered in the cell
        player_center = (
            player_pos[1] * CELL_SIZE + CELL_SIZE // 2,
            player_pos[0] * CELL_SIZE + CELL_SIZE // 2 + STATS_PANEL_HEIGHT,
        )
        pygame.draw.circle(self.screen, COLOR_MAPPINGS["PLAYER"], player_center, CELL_SIZE // 2 - 2)
