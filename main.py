import pygame
import random
from time import sleep

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = 300, 300
BACKGROUND = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
X_ICON_FILEPATH = 'Assets/x_icon.png'
O_ICON_FILEPATH = 'Assets/o_icon.png'
FPS = 60
GAME_OVER = False
BOARD = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
PLAYER_TURN = True
MOVES = 0
MAX_MOVES = 9
pygame.init()

my_font = pygame.font.SysFont("Courier New", 30)

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
GAME_ICON = pygame.image.load('Assets/game_icon.png')
pygame.display.set_icon(GAME_ICON)


def init_game(grid):
    global GAME_OVER, BOARD, PLAYER_TURN, MOVES, MAX_MOVES
    grid = draw_grid()
    GAME_OVER = False
    BOARD = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    PLAYER_TURN = True
    MOVES = 0
    MAX_MOVES = 9


def draw_grid():
    WINDOW.fill(BACKGROUND)
    x = (WINDOW_WIDTH - GRID_WIDTH - 3) // 2
    y = (WINDOW_HEIGHT - GRID_HEIGHT - 3) // 2
    grid = pygame.Rect((x, y, GRID_WIDTH, GRID_HEIGHT))
    pygame.draw.rect(WINDOW, BLACK, grid,
                     3)  # pygame.draw.rect(surface, color, (x,y,width,height))
    pygame.draw.line(WINDOW, (0, 0, 0), (grid.x + GRID_WIDTH / 3, grid.y), (grid.x + GRID_WIDTH / 3, grid.bottom))
    pygame.draw.line(WINDOW, (0, 0, 0), (grid.x + 2 * GRID_WIDTH / 3, grid.y),
                     (grid.x + 2 * GRID_WIDTH / 3, grid.bottom))
    pygame.draw.line(WINDOW, (0, 0, 0), (grid.x, grid.y + GRID_HEIGHT / 3),
                     (grid.x + GRID_WIDTH, grid.y + GRID_HEIGHT / 3))
    pygame.draw.line(WINDOW, (0, 0, 0), (grid.x, grid.y + 2 * GRID_HEIGHT / 3),
                     (grid.x + GRID_WIDTH, grid.y + 2 * GRID_HEIGHT / 3))

    pygame.display.update()
    return grid


def check_draw(grid):
    global GAME_OVER
    draw = False
    if MOVES == MAX_MOVES and not check_winner(grid, 'X') and not check_winner(grid, 'O') and not has_space():
        GAME_OVER = True
        draw = True
    return draw


def has_space():
    global BOARD
    space = False
    for row in range(3):
        for col in range(3):
            if BOARD[row][col] == '-':
                space = True

    return space


def cpu_turn(grid):
    global BOARD, PLAYER_TURN, MOVES

    r = random.randint(0, 2)
    c = random.randint(0, 2)

    if has_space():
        while BOARD[r][c] != '-':
            r = random.randint(0, 2)
            c = random.randint(0, 2)

        if c == 0:
            col = grid.x

        elif c == 1:
            col = grid.x + GRID_WIDTH / 3

        else:
            col = grid.x + 2 * GRID_WIDTH / 3

        if r == 0:
            row = grid.y

        elif r == 1:
            row = grid.y + GRID_HEIGHT / 3

        else:
            row = grid.y + 2 * GRID_HEIGHT / 3

        BOARD[r][c] = 'O'
        sleep(0.5)
        draw_icon(col + 5, row + 5, O_ICON_FILEPATH)
        MOVES += 1
        PLAYER_TURN = True


def take_turns(mouse_x, mouse_y, grid):
    global BOARD, PLAYER_TURN, MOVES
    offset_x = mouse_x - grid.x
    offset_y = mouse_y - grid.y

    if offset_x <= GRID_WIDTH / 3:
        c = 0
        col = grid.x

    elif offset_x <= 2 * GRID_WIDTH / 3:
        c = 1
        col = grid.x + GRID_WIDTH / 3

    else:
        c = 2
        col = grid.x + 2 * GRID_WIDTH / 3

    if offset_y <= GRID_HEIGHT / 3:
        r = 0
        row = grid.y

    elif offset_y <= 2 * GRID_HEIGHT / 3:
        r = 1
        row = grid.y + GRID_HEIGHT / 3

    else:
        r = 2
        row = grid.y + 2 * GRID_HEIGHT / 3

    if PLAYER_TURN and BOARD[r][c] == '-' and has_space():
        BOARD[r][c] = 'X'
        draw_icon(col + 5, row + 5, X_ICON_FILEPATH)
        MOVES += 1
        PLAYER_TURN = False
        if not check_winner(grid, 'X'):
            # cpu turn
            cpu_turn(grid)
            check_winner(grid, 'O')


def handle_mouse_event(grid):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if grid.collidepoint(mouse_x, mouse_y):
        take_turns(mouse_x, mouse_y, grid)


def print_board():
    for row in BOARD:
        print("".join(row))


def draw_line(start_coord, end_coord):
    pygame.draw.line(WINDOW, RED, start_coord, end_coord, 5)
    pygame.display.update()


def check_winner(grid, player):
    global GAME_OVER
    winner = False

    # leading diagonal
    if BOARD[0][0] == player and BOARD[1][1] == BOARD[0][0] and BOARD[1][1] == BOARD[2][2]:
        draw_line(grid.topleft, grid.bottomright)
        winner = True
        GAME_OVER = True

    # other diagonal
    if BOARD[0][2] == player and BOARD[1][1] == BOARD[0][2] and BOARD[1][1] == BOARD[2][0]:
        draw_line(grid.topright, grid.bottomleft)
        winner = True
        GAME_OVER = True

    # first row
    if BOARD[0][0] == player and BOARD[0][1] == BOARD[0][0] and BOARD[0][1] == BOARD[0][2]:
        y1 = grid.y + (GRID_HEIGHT / 6)
        x1 = grid.x

        x2 = grid.right
        y2 = y1
        draw_line((x1, y1), (x2, y2))
        winner = True
        GAME_OVER = True

    # second row
    if BOARD[1][0] == player and BOARD[1][1] == BOARD[1][0] and BOARD[1][1] == BOARD[1][2]:
        y1 = grid.y + (GRID_HEIGHT / 2)
        x1 = grid.x

        x2 = grid.right
        y2 = y1
        draw_line((x1, y1), (x2, y2))
        winner = True
        GAME_OVER = True

    # third row
    if BOARD[2][0] == player and BOARD[2][1] == BOARD[2][0] and BOARD[2][1] == BOARD[2][2]:
        y1 = grid.y + (5 * GRID_HEIGHT / 6)
        x1 = grid.x

        x2 = grid.right
        y2 = y1
        draw_line((x1, y1), (x2, y2))

        winner = True
        GAME_OVER = True

    # first column
    if BOARD[0][0] == player and BOARD[1][0] == BOARD[0][0] and BOARD[1][0] == BOARD[2][0]:
        y1 = grid.y
        x1 = grid.x + (GRID_WIDTH / 6)

        x2 = x1
        y2 = grid.bottom
        draw_line((x1, y1), (x2, y2))
        winner = True
        GAME_OVER = True

    # second column
    if BOARD[0][1] == player and BOARD[1][1] == BOARD[0][1] and BOARD[1][1] == BOARD[2][1]:
        y1 = grid.y
        x1 = grid.x + (GRID_WIDTH / 2)

        x2 = x1
        y2 = grid.bottom
        draw_line((x1, y1), (x2, y2))
        winner = True
        GAME_OVER = True

    # third column
    if BOARD[0][2] == player and BOARD[1][2] == BOARD[0][2] and BOARD[1][2] == BOARD[2][2]:
        y1 = grid.y
        x1 = grid.x + (5 * GRID_WIDTH / 6)

        x2 = x1
        y2 = grid.bottom
        draw_line((x1, y1), (x2, y2))
        winner = True
        GAME_OVER = True

    return winner


def draw_icon(x, y, filepath):
    # x_icon = pygame.image.load('Assets/x_icon.png')
    icon = pygame.image.load(filepath)
    image = pygame.transform.scale(icon, (80, 80))
    WINDOW.blit(image, (x, y))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    grid = draw_grid()
    exited = False

    while not exited:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and PLAYER_TURN and not GAME_OVER:
                handle_mouse_event(grid)
                print_board()
                check_draw(grid)
                print("\n")

            if GAME_OVER:
                txt = my_font.render('GAME OVER!', True, RED)
                x = int((WINDOW.get_width() - txt.get_width()) / 2)
                y = grid.y - 50
                WINDOW.blit(txt, (x, y))

                if check_winner(grid, 'O'):
                    msg = "CPU WINS :("
                    color = RED
                elif check_winner(grid, 'X'):
                    msg = "YOU WIN!"
                    color = GREEN

                else:
                    msg = "IT'S A DRAW!"
                    color = GREEN

                txt = my_font.render(msg, True, color)
                x = int((WINDOW.get_width() - txt.get_width()) / 2)
                y = grid.bottom + 30
                WINDOW.blit(txt, (x, y))

                txt = my_font.render('PLAY ANOTHER GAME? (Y\\N)', True, BLUE)
                x = int((WINDOW.get_width() - txt.get_width()) / 2)
                y = grid.bottom + 75
                WINDOW.blit(txt, (x, y))

                pygame.display.update()

                if event.type == pygame.KEYDOWN:
                    # Rematch
                    if event.key == pygame.K_y:
                        init_game(grid)

                    # Quit
                    elif event.key == pygame.K_n:
                        exited = True

    pygame.quit()


if __name__ == '__main__':
    main()
