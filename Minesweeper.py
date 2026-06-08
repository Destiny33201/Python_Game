import pygame
import random
import sys

pygame.init()

# -----------------------------
# SETTINGS
# -----------------------------
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
CELL_SIZE = WIDTH // GRID_SIZE

MINE_COUNT = 99

# -----------------------------
# COLORS
# -----------------------------
BG_COLOR = (30, 30, 30)
LINE_COLOR = (200, 200, 200)
REVEALED_COLOR = (120, 120, 120)
FLAG_COLOR = (255, 255, 0)
MINE_COLOR = (255, 0, 0)

# -----------------------------
# GAME DATA
# -----------------------------
board = []
revealed = []
flagged = []

game_over = False
game_won = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

font = pygame.font.SysFont(None, 20)

# -----------------------------
# BOARD GENERATION
# -----------------------------
def create_board():

    global board
    global revealed
    global flagged
    global game_over
    global game_won

    game_over = False
    game_won = False

    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    revealed = [
        [False for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]

    flagged = [
        [False for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]

    # Place mines
    placed = 0

    while placed < MINE_COUNT:

        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)

        if board[row][col] != -1:
            board[row][col] = -1
            placed += 1

    # Calculate numbers
    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            if board[row][col] == -1:
                continue

            count = 0

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:

                    nr = row + dr
                    nc = col + dc

                    if (
                        0 <= nr < GRID_SIZE and
                        0 <= nc < GRID_SIZE
                    ):

                        if board[nr][nc] == -1:
                            count += 1

            board[row][col] = count


# -----------------------------
# FLOOD FILL
# -----------------------------
def reveal_cell(row, col):

    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
        return

    if revealed[row][col]:
        return

    if flagged[row][col]:
        return

    revealed[row][col] = True

    if board[row][col] != 0:
        return

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:

            if dr == 0 and dc == 0:
                continue

            reveal_cell(row + dr, col + dc)


# -----------------------------
# WIN CHECK
# -----------------------------
def check_win():

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            if board[row][col] != -1 and not revealed[row][col]:
                return False

    return True


# -----------------------------
# DRAWING
# -----------------------------
def draw_grid():

    screen.fill(BG_COLOR)

    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            rect = pygame.Rect(
                x,
                y,
                CELL_SIZE,
                CELL_SIZE
            )

            # Revealed cells
            if revealed[row][col]:

                pygame.draw.rect(
                    screen,
                    REVEALED_COLOR,
                    rect
                )

                value = board[row][col]

                # Mine
                if value == -1:

                    pygame.draw.circle(
                        screen,
                        MINE_COLOR,
                        (
                            x + CELL_SIZE // 2,
                            y + CELL_SIZE // 2
                        ),
                        CELL_SIZE // 3
                    )

                # Number
                elif value > 0:

                    text = font.render(
                        str(value),
                        True,
                        (255, 255, 255)
                    )

                    screen.blit(
                        text,
                        (
                            x + CELL_SIZE // 4,
                            y + CELL_SIZE // 8
                        )
                    )

            # Flag
            elif flagged[row][col]:

                pygame.draw.rect(
                    screen,
                    FLAG_COLOR,
                    (
                        x + 4,
                        y + 4,
                        CELL_SIZE - 8,
                        CELL_SIZE - 8
                    )
                )

            pygame.draw.rect(
                screen,
                LINE_COLOR,
                rect,
                1
            )


# -----------------------------
# MAIN
# -----------------------------
def main():

    global game_over
    global game_won

    create_board()

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Restart
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    create_board()

            if game_over or game_won:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE

                # Left click
                if event.button == 1:

                    if not flagged[row][col]:

                        if board[row][col] == -1:

                            game_over = True

                            for r in range(GRID_SIZE):
                                for c in range(GRID_SIZE):
                                    if board[r][c] == -1:
                                        revealed[r][c] = True

                            print("Game Over! Press R to restart.")

                        else:

                            reveal_cell(row, col)

                            if check_win():

                                game_won = True
                                print("You Win! Press R to restart.")

                # Right click
                elif event.button == 3:

                    if not revealed[row][col]:

                        flagged[row][col] = (
                            not flagged[row][col]
                        )

        draw_grid()

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main() 