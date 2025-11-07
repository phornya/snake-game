import pygame
from pygame.math import Vector2
from .settings import cell_size

#Grid setup
try:
    from .settings import cell_number
    CELL_NUMBER_X = CELL_NUMBER_Y = cell_number
except Exception:
    CELL_NUMBER_X = 30
    CELL_NUMBER_Y = 25


class SNAKE:
    def __init__(self, screen, sound_folder="sound"):
        self.screen = screen
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        #Load images
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
        except Exception as e:
            print("⚠️ Image load error:", e)
            # fallback simple colored blocks
            surf = pygame.Surface((cell_size, cell_size))
            surf.fill((0, 200, 0))
            self.head_up = self.head_down = self.head_right = self.head_left = surf
            tail_surf = pygame.Surface((cell_size, cell_size))
            tail_surf.fill((0, 180, 0))
            self.tail_up = self.tail_down = self.tail_right = self.tail_left = tail_surf
            body_surf = pygame.Surface((cell_size, cell_size))
            body_surf.fill((0, 160, 0))
            self.body_vertical = self.body_horizontal = self.body_tr = self.body_tl = self.body_br = self.body_bl = body_surf

        # default orientation
        self.head = self.head_right
        self.tail = self.tail_left

        # sound
        try:
            self.crunch_sound = pygame.mixer.Sound(f"{sound_folder}/crunch.wav")
        except Exception:
            self.crunch_sound = None

    #Helpers
    def _wrap_position(self, vec):
        return Vector2(vec.x % CELL_NUMBER_X, vec.y % CELL_NUMBER_Y)

    def _get_direction(self, from_block, to_block):
        diff = Vector2(to_block.x - from_block.x, to_block.y - from_block.y)

        if diff.x > CELL_NUMBER_X / 2:
            diff.x -= CELL_NUMBER_X
        elif diff.x < -CELL_NUMBER_X / 2:
            diff.x += CELL_NUMBER_X
        if diff.y > CELL_NUMBER_Y / 2:
            diff.y -= CELL_NUMBER_Y
        elif diff.y < -CELL_NUMBER_Y / 2:
            diff.y += CELL_NUMBER_Y

        return Vector2(int(diff.x), int(diff.y))

    #Draw
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
                prev_dir = self._get_direction(block, self.body[index + 1])
                next_dir = self._get_direction(block, self.body[index - 1])

                if prev_dir.x == next_dir.x:
                    self.screen.blit(self.body_vertical, block_rect)
                elif prev_dir.y == next_dir.y:
                    self.screen.blit(self.body_horizontal, block_rect)
                else:
                    if (prev_dir.x == -1 and next_dir.y == -1) or (prev_dir.y == -1 and next_dir.x == -1):
                        self.screen.blit(self.body_tl, block_rect)
                    elif (prev_dir.x == -1 and next_dir.y == 1) or (prev_dir.y == 1 and next_dir.x == -1):
                        self.screen.blit(self.body_bl, block_rect)
                    elif (prev_dir.x == 1 and next_dir.y == -1) or (prev_dir.y == -1 and next_dir.x == 1):
                        self.screen.blit(self.body_tr, block_rect)
                    elif (prev_dir.x == 1 and next_dir.y == 1) or (prev_dir.y == 1 and next_dir.x == 1):
                        self.screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        if len(self.body) < 2:
            return
        head_relation = self._get_direction(self.body[0], self.body[1])
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
        tail_relation = self._get_direction(self.body[-2], self.body[-1])
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_up

    #Movement
    def move_snake(self):
        body_copy = self.body[:]
        new_head = body_copy[0] + self.direction
        new_head = self._wrap_position(new_head)
        body_copy.insert(0, new_head)

        if not self.new_block:
            body_copy = body_copy[:-1]

        self.body = body_copy
        self.new_block = False

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        if self.crunch_sound:
            self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
