import pygame
import random
from game import Game, GameModesType, InputType
from renderer import Renderer, STATS_PANEL_HEIGHT

pygame.init()


def handle_keybinds(event_key: int, game: Game):
    if event_key == pygame.K_r:
        game.reset()

    if event_key == pygame.K_m:
        game.mode = GameModesType.TRAINING if game.mode == GameModesType.MANUAL else GameModesType.MANUAL

    if game.mode == GameModesType.MANUAL:
        mappings = {
            pygame.K_w: InputType.MOVE_UP,
            pygame.K_UP: InputType.MOVE_UP,
            pygame.K_a: InputType.MOVE_LEFT,
            pygame.K_LEFT: InputType.MOVE_LEFT,
            pygame.K_s: InputType.MOVE_DOWN,
            pygame.K_DOWN: InputType.MOVE_DOWN,
            pygame.K_d: InputType.MOVE_RIGHT,
            pygame.K_RIGHT: InputType.MOVE_RIGHT,
        }

        if event_key in mappings:
            game.handle_input(mappings[event_key])
    return None


def main():
    # Initialize the game with a random grid size
    game = Game(7)

    # Create a shell to initialize the renderer
    shell = pygame.Surface((1, 1))
    renderer = Renderer(shell, game)

    # Create the actual screen with the correct screen size
    screen = pygame.display.set_mode((renderer.window_size, renderer.window_size + STATS_PANEL_HEIGHT))
    pygame.display.set_caption(f"Grid Game - Size: 7x7")

    # Update the screen in the renderer
    renderer.screen = screen

    clock = pygame.time.Clock()
    training_timer = 0
    training_interval = 50  # milliseconds between training

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keybinds(event.key, game)

        # Run training
        if game.mode == GameModesType.TRAINING:
            current_time = pygame.time.get_ticks()
            if current_time - training_timer >= training_interval:
                game.auto_move()
                training_timer = current_time

        renderer.draw()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
