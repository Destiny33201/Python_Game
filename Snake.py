import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window settings
WIDTH = 800
HEIGHT = 900
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Colors
BG_COLOR = (40, 40, 40)
SNAKE_COLOR = (0, 255, 100)
FOOD_COLOR = (255, 0, 0)

# Snake setup
snake = [
    [10, 10]
]

growth = 0

direction_x = 1
direction_y = 0

# Food setup
food = [
    random.randint(0, WIDTH // CELL_SIZE - 1),
    random.randint(0, HEIGHT // CELL_SIZE - 1)
]

# Movement timing
MOVE_DELAY = 150  # milliseconds
move_timer = 0

running = True

while running:

    # -------------------------
    # EVENT HANDLING
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == (pygame.K_a) and direction_x != 1:
                direction_x = -1
                direction_y = 0

            elif event.key == (pygame.K_d) and direction_x != -1:
                direction_x = 1
                direction_y = 0

            elif event.key == (pygame.K_w) and direction_y != 1:
                direction_x = 0
                direction_y = -1

            elif event.key == (pygame.K_s) and direction_y != -1:
                direction_x = 0
                direction_y = 1

    # -------------------------
    # MOVE SNAKE
    # -------------------------
    move_timer += clock.get_time()

    if move_timer >= MOVE_DELAY:

        move_timer = 0

        new_head = [
            snake[0][0] + direction_x,
            snake[0][1] + direction_y
        ]

        snake.insert(0, new_head)

        # Food collision
        if snake[0] == food:

            growth += 3

            while True:
                food = [
                    random.randint(0, WIDTH // CELL_SIZE - 1),
                    random.randint(0, HEIGHT // CELL_SIZE - 1)
                ]
                if food not in snake:
                    break

        if growth > 0:
            growth -= 1
        else:
            snake.pop()

        # Wall collision
        head_x = snake[0][0]
        head_y = snake[0][1]

        if (
            head_x < 0 or
            head_x >= WIDTH // CELL_SIZE or
            head_y < 0 or
            head_y >= HEIGHT // CELL_SIZE
        ):
            print("Game Over! Hit a wall.")
            running = False

        # Self collision
        if snake[0] in snake[1:]:
            print("Game Over! Hit yourself.")
            running = False

    # -------------------------
    # DRAW
    # -------------------------
    screen.fill(BG_COLOR)

    # Draw food
    pygame.draw.rect(
        screen,
        FOOD_COLOR,
        (
            food[0] * CELL_SIZE,
            food[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # Draw snake
    for segment in snake:
        pygame.draw.rect(
            screen,
            SNAKE_COLOR,
            (
                segment[0] * CELL_SIZE,
                segment[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()