import pygame
import sys
from snake import Snake, SnakeFragment
from fruit import Fruit

pygame.init()

# CONST VALUES
SCREEN_WIDTH = 800
SCREEN_WIDTH_SQUARES = SCREEN_WIDTH // 40
SCREEN_HEIGHT = 600
SCREEN_HEIGHT_SQUARES = SCREEN_HEIGHT // 40
SQUARE_SIZE = 40
GREEN = (38, 173, 40)
LIGHT_GREEN = (100, 250, 102)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

def draw_screen(snake, fruit):
    screen.fill(LIGHT_GREEN)

    for row in range(SCREEN_HEIGHT_SQUARES):
        for col in range(SCREEN_WIDTH_SQUARES):
            if (row + col) % 2 == 0:
                color = GREEN
            else:
                color = LIGHT_GREEN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    fruit.draw(screen)
    snake.draw(screen)

    pygame.display.flip()

def handle_movement_keys(snake):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake.change_direction('w')
    if keys[pygame.K_d]:
        snake.change_direction('d')
    if keys[pygame.K_s]:
        snake.change_direction('s')
    if keys[pygame.K_a]:
        snake.change_direction('a')

def main():

    snake = Snake(SCREEN_HEIGHT_SQUARES, SCREEN_WIDTH_SQUARES, SQUARE_SIZE)
    fruit = Fruit(SCREEN_HEIGHT_SQUARES, SCREEN_WIDTH_SQUARES, SQUARE_SIZE)

    fruits = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_movement_keys(snake)
        snake.move()

        if not fruits:
            fruits += 1
            fruit.refresh()

        draw_screen(snake, fruit)

        if not snake.check():
            break

        clock.tick(10)

    pygame.quit()
    sys.exit()

main()