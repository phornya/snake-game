import pygame
import sys
from pygame.math import Vector2
from snake.game import Main
from snake.settings import cell_size, cell_number


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


main_game = Main(screen, game_font, apple_image=apple, sound_folder="sound")

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 160)

# Menu
def draw_text_center(surface, text, font, y, color=(255, 255, 255)):
    txt_surf = font.render(text, True, color)
    txt_rect = txt_surf.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(txt_surf, txt_rect)

def draw_button(surface, rect, text, font, hovered=False):
    border_color = (255, 255, 255)
    bg_color = (100, 149, 237) if not hovered else (140, 219, 217)
    pygame.draw.rect(surface, bg_color, rect, border_radius=8)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=8)
    txt = font.render(text, True, (255, 255, 255))
    txt_rect = txt.get_rect(center=rect.center)
    surface.blit(txt, txt_rect)

def create_buttons(surface):
    w = surface.get_width()
    h = surface.get_height()
    btn_w, btn_h = w // 3, 40
    start_rect = pygame.Rect((w//2 - btn_w//2, h//2 - 20 - btn_h), (btn_w, btn_h))
    instr_rect = pygame.Rect((w//2 - btn_w//2, h//2 + 30 - btn_h), (btn_w, btn_h))
    quit_rect = pygame.Rect((w//2 - btn_w//2, h//2 + 80 - btn_h), (btn_w, btn_h))
    return {"start": start_rect, "instructions": instr_rect, "quit game": quit_rect}

buttons = create_buttons(screen)
state = "menu"
show_instructions = False
instructions_lines = [
    "Controls:",
    "- Arrow keys or WASD to move",
    "- Press R to restart when game over",
    "- Eat apples to grow and increase score",
    "",
    "Press Enter or click Start to play.",
    "Press Q to quit, I to toggle this help."
]

def create_gameover_buttons(surface):
    w = surface.get_width()
    btn_w, btn_h = w // 4, 42
    center_x = w // 2 - btn_w // 2
    y_start = surface.get_height() // 2 + 40
    restart_rect = pygame.Rect((center_x, y_start), (btn_w, btn_h))
    menu_rect = pygame.Rect((center_x, y_start + 56), (btn_w, btn_h))
    quit_rect = pygame.Rect((center_x, y_start + 112), (btn_w, btn_h))
    return {"restart": restart_rect, "menu": menu_rect, "quit game": quit_rect}

gameover_buttons = create_gameover_buttons(screen)

# Main loop with Menu
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if state == "playing":
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                # controls
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
                # return to menu
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
                break

            # handle clicks on the buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and main_game.is_game_over:
                if gameover_buttons["restart"].collidepoint(mouse_pos):
                    main_game.reset()
                elif gameover_buttons["menu"].collidepoint(mouse_pos):
                    state = "menu"
                elif gameover_buttons["quit game"].collidepoint(mouse_pos):
                    running = False
                    break

        else:
            #  instruction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    main_game.reset()
                    state = "playing"
                if event.key == pygame.K_i:
                    show_instructions = not show_instructions
                    state = "instructions" if show_instructions else "menu"
                if event.key == pygame.K_q:
                    running = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons["start"].collidepoint(mouse_pos):
                    main_game.reset()
                    state = "playing"
                elif buttons["instructions"].collidepoint(mouse_pos):
                    show_instructions = True
                    state = "instructions"
                elif buttons["quit game"].collidepoint(mouse_pos):
                    running = False
                    break

    # Render on state
    if state == "menu":
        screen.fill((42, 212, 116))
        draw_text_center(screen, "SNAKE GAME !", pygame.font.Font(None, 72), screen.get_height()//4)
        draw_text_center(screen, "get start funny game", pygame.font.Font(None, 24), screen.get_height()//4 + 50)

        # draw buttons
        for name, rect in buttons.items():
            hovered = rect.collidepoint(mouse_pos)
            label = name.capitalize()
            if name == "quit game":
                label = "Quit game"
            if name == "instructions":
                label = "Instructions"
            draw_button(screen, rect, label, game_font, hovered=hovered)

        draw_text_center(screen, "Click to Start Play Now and Stop It", game_font, screen.get_height() - 30, color=(80, 80, 80))

    elif state == "instructions":
        screen.fill((18, 18, 30))
        draw_text_center(screen, "How to Play", pygame.font.Font(None, 56), screen.get_height()//6)

        start_y = screen.get_height()//6 + 60
        for i, line in enumerate(instructions_lines):
            txt = game_font.render(line, True, (230, 230, 230))
            txt_rect = txt.get_rect(center=(screen.get_width()//2, start_y + i * 28))
            screen.blit(txt, txt_rect)

        draw_text_center(screen, "Click anywhere or press I to go back", game_font, screen.get_height() - 40, color=(150,150,150))

        if pygame.mouse.get_pressed()[0]:
            show_instructions = False
            state = "menu"

    elif state == "playing":
        main_game.draw_elements()


        if main_game.is_game_over:
            
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            score_text = ""
            score_val = None

            if hasattr(main_game, "score"):
                try:
                    score_val = getattr(main_game, "score")
                except Exception:
                    score_val = None
            elif hasattr(main_game, "get_score"):
                try:
                    score_val = main_game.get_score()
                except Exception:
                    score_val = None
            else:

                try:
                    score_val = len(main_game.snake.body) - 3 
                except Exception:
                    score_val = None

            if score_val is not None:
                score_text = f"Score: {score_val}"
                pygame.display.set_caption(f"SNAKE GAME - Game Over - {score_text}")
            else:
                pygame.display.set_caption("SNAKE GAME - Game Over")

            draw_text_center(screen, "You Failed!", pygame.font.Font(None, 64), screen.get_height()//2 - 40)
            draw_text_center(screen, "Click Restart or press R to play again", game_font, screen.get_height()//2 + 6)

            # Draw buttons
            for name, rect in gameover_buttons.items():
                hovered = rect.collidepoint(mouse_pos)
                label = name.capitalize()
                draw_button(screen, rect, label, game_font, hovered=hovered)

    # update and display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
