import pygame
import random
from pygame.math import Vector2
from .settings import cell_size, cell_number

class Fruit:
    def __init__(self, screen, apple_image=None):
        self.screen = screen
        self.apple = apple_image
        self.random_position()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        try:
            if self.apple:
                self.screen.blit(self.apple, fruit_rect)
            else:
                pygame.draw.rect(self.screen, (255, 0, 0), fruit_rect)
        except Exception:
            pygame.draw.rect(self.screen, (255, 0, 0), fruit_rect)

    def random_position(self, snake_body=None):
        while True:
            pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
            if snake_body and pos in snake_body:
                continue
            self.pos = pos
            break
