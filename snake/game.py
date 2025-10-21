import pygame
from .snake import SNAKE
from .food import Fruit
from .settings import cell_size, cell_number

class Main:
    def __init__(self, screen, game_font, apple_image=None, sound_folder="sound"):
        self.screen = screen
        self.game_font = game_font
        self.snake = SNAKE(screen, sound_folder=sound_folder)
        self.fruit = Fruit(screen, apple_image)
        self.fruit.random_position(self.snake.body)
        self.is_game_over = False
        self.score = 0

    def update(self):
        if not self.is_game_over:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        if not self.is_game_over:
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
        else:
            self.draw_game_over()

    def check_collision(self):
        # head eats fruit
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random_position(self.snake.body)
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1

        # if fruit spawns on snake (rare), move it
        for block in self.snake.body:
            if block == self.fruit.pos:
                self.fruit.random_position(self.snake.body)
                break

    def check_fail(self):
        head = self.snake.body[0]
        if not (0 <= head.x < cell_number and 0 <= head.y < cell_number):
            self.is_game_over = True
        for block in self.snake.body[1:]:
            if block == head:
                self.is_game_over = True
                break

    def draw_grass(self):
        light_grass = (167, 209, 61)
        dark_grass = (170, 215, 70)
        for row in range(cell_number):
            for col in range(cell_number):
                color = light_grass if (row + col) % 2 == 0 else dark_grass
                pygame.draw.rect(self.screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    def draw_score(self):
        score_surface = self.game_font.render(f"Score: {self.score}", True, (56, 74, 12))
        self.screen.blit(score_surface, (10, 10))

    def draw_game_over(self):
        over_text = self.game_font.render("SNAKE GAME OVER", True, (255, 0, 0))
        restart_text = self.game_font.render("Press R to Again", True, (56, 74, 12))
        score_text = self.game_font.render(f"Your Score: {self.score}", True, (0, 0, 0))
        self.screen.fill((175, 215, 70))
        self.screen.blit(over_text, over_text.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2 - 40)))
        self.screen.blit(score_text, score_text.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2 + 40)))

    def reset(self):
        self.snake.reset()
        self.fruit.random_position(self.snake.body)
        self.is_game_over = False
        self.score = 0
