import pygame
import sys
from pygame.math import Vector2
from snake.game import Main
from snake.settings import cell_size, cell_number

# Config & init
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

SCREEN_SIZE = (cell_number * cell_size, cell_number * cell_size)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Try to load assets
try:
    apple = pygame.image.load('assets/food.png').convert_alpha()
except Exception:
    apple = None

try:
    game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)
except Exception:
    game_font = pygame.font.SysFont('Arial', 25)

# Create game instance and timer
main_game = Main(screen, game_font, apple_image=apple, sound_folder="sound")

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if main_game.is_game_over and event.key == pygame.K_r:
                main_game.reset()
            if not main_game.is_game_over:
                if event.key in [pygame.K_UP, pygame.K_w] and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key in [pygame.K_DOWN, pygame.K_s] and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key in [pygame.K_LEFT, pygame.K_a] and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                if event.key in [pygame.K_RIGHT, pygame.K_d] and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
