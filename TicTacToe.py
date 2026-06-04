import pygame
import sys

# Initialize Pygame
pygame.init()

# Window dimensions & grid settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
BG_COLOR = (30, 30, 30)
LINE_COLOR = (200, 200, 200)
X_COLOR = (255, 100, 100)
O_COLOR = (100, 150, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Board state
board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

current_player = "X"
game_over = False


def draw_grid():
    """Draw the board and pieces."""
    screen.fill(BG_COLOR)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Draw border
            pygame.draw.rect(screen, LINE_COLOR, rect, 2)

            # Draw X
            if board[row][col] == "X":
                padding = 40

                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (x + padding, y + padding),
                    (x + CELL_SIZE - padding, y + CELL_SIZE - padding),
                    5
                )

                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (x + CELL_SIZE - padding, y + padding),
                    (x + padding, y + CELL_SIZE - padding),
                    5
                )

            # Draw O
            elif board[row][col] == "O":
                pygame.draw.circle(
                    screen,
                    O_COLOR,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    CELL_SIZE // 3,
                    5
                )

def restart_game():
    global board
    global current_player
    global game_over

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    current_player = "X"
    game_over = False

    print("Game restarted!")

def check_winner():
    """Returns X, O, Draw, or None."""

    # Check rows
    for row in range(3):
        if (
            board[row][0] != ""
            and board[row][0] == board[row][1] == board[row][2]
        ):
            return board[row][0]

    # Check columns
    for col in range(3):
        if (
            board[0][col] != ""
            and board[0][col] == board[1][col] == board[2][col]
        ):
            return board[0][col]

    # Main diagonal
    if (
        board[0][0] != ""
        and board[0][0] == board[1][1] == board[2][2]
    ):
        return board[0][0]

    # Other diagonal
    if (
        board[0][2] != ""
        and board[0][2] == board[1][1] == board[2][0]
    ):
        return board[0][2]

    # Draw check
    full = True

    for row in board:
        for cell in row:
            if cell == "":
                full = False

    if full:
        return "Draw"

    return None


def main():
    global current_player
    global game_over

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #pygame.K_(insert whatever key you want to be the action)
                    restart_game()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and not game_over
            ):

                mouse_x, mouse_y = pygame.mouse.get_pos()

                clicked_col = mouse_x // CELL_SIZE
                clicked_row = mouse_y // CELL_SIZE

                # Only place if empty
                if board[clicked_row][clicked_col] == "":

                    board[clicked_row][clicked_col] = current_player

                    winner = check_winner()

                    if winner:

                        game_over = True

                        if winner == "Draw":
                            print("Draw! Press R to restart.")
                        else:
                            print(f"{winner} wins! Press R to restart.")

                    else:
                        if current_player == "X":
                            current_player = "O"
                        else:
                            current_player = "X"

        draw_grid()

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()