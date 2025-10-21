import pygame
from pygame.math import Vector2
from .settings import cell_size

class SNAKE:
    def __init__(self, screen, sound_folder="sound"):
        # screen passed from main
        self.screen = screen
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        # load images
        try:
            self.head_up = pygame.image.load("assets/head_up.png").convert_alpha()
            self.head_down = pygame.image.load("assets/head_down.png").convert_alpha()
            self.head_right = pygame.image.load("assets/head_right.png").convert_alpha()
            self.head_left = pygame.image.load("assets/head_left.png").convert_alpha()

            self.tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()
            self.tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
            self.tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()
            self.tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()

            self.body_vertical = pygame.image.load("assets/body_vertical.png").convert_alpha()
            self.body_horizontal = pygame.image.load("assets/body_horizontal.png").convert_alpha()

            self.body_tr = pygame.image.load("assets/body_tr.png").convert_alpha()
            self.body_tl = pygame.image.load("assets/body_tl.png").convert_alpha()
            self.body_br = pygame.image.load("assets/body_br.png").convert_alpha()
            self.body_bl = pygame.image.load("assets/body_bl.png").convert_alpha()
        except Exception:
            # fallback surfaces if images missing
            surf = pygame.Surface((cell_size, cell_size))
            surf.fill((0, 200, 0))
            self.head_up = self.head_down = self.head_right = self.head_left = surf
            tail_surf = pygame.Surface((cell_size, cell_size))
            tail_surf.fill((0, 180, 0))
            self.tail_up = self.tail_down = self.tail_right = self.tail_left = tail_surf
            body_surf = pygame.Surface((cell_size, cell_size))
            body_surf.fill((0, 160, 0))
            self.body_vertical = self.body_horizontal = self.body_tr = self.body_tl = self.body_br = self.body_bl = body_surf

        # sound
        try:
            self.crunch_sound = pygame.mixer.Sound(f"{sound_folder}/crunch.wav")
        except Exception:
            self.crunch_sound = None

        # images default
        self.head = self.head_right
        self.tail = self.tail_left

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                self.screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                self.screen.blit(self.tail, block_rect)
            else:
                prev_block = self.body[index + 1] - block   # block towards tail and head
                next_block = self.body[index - 1] - block  

                if prev_block.x == next_block.x:
                    self.screen.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal, block_rect)
                else:
                    # corner
                    if (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
                        self.screen.blit(self.body_tl, block_rect)
                    elif (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
                        self.screen.blit(self.body_bl, block_rect)
                    elif (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
                        self.screen.blit(self.body_tr, block_rect)
                    elif (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1):
                        self.screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        # relation from head to second
        if len(self.body) < 2:
            return
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        if len(self.body) < 2:
            return
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        
    def play_crunch_sound(self):
        if self.crunch_sound:
            self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        
