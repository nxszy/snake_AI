import pygame
import sys
from snake import Snake, SnakeFragment
from fruit import Fruit

pygame.init()

# CONST VALUES
SCREEN_WIDTH = 800
SCREEN_WIDTH_SQUARES = SCREEN_WIDTH // 40
SCREEN_HEIGHT = 640
SCREEN_HEIGHT_SQUARES = SCREEN_HEIGHT // 40
SQUARE_SIZE = 40
GREEN = (38, 173, 40)
LIGHT_GREEN = (100, 250, 102)
GRAY = (116, 128, 119)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

def draw_screen(snake, fruit, score):
    screen.fill(LIGHT_GREEN)

    for row in range(SCREEN_HEIGHT_SQUARES):
        for col in range(SCREEN_WIDTH_SQUARES):
            if (row == 0):
                color = GRAY
            elif (row + col) % 2 == 0:
                color = GREEN
            else:
                color = LIGHT_GREEN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    text = font.render(f"Score: {score}", True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, 20)

    # Blit the text onto the screen
    screen.blit(text, text_rect)

    if fruit:
        fruit.draw(screen)

    snake.draw(screen)

    pygame.display.flip()

def handle_movement_keys(snake):
    keys = pygame.key.get_pressed()
    print(keys[pygame.K_w], snake.direction)
    if keys[pygame.K_w] and snake.direction.name != 'S':
        snake.change_direction('w')
    if keys[pygame.K_d] and snake.direction.name != 'A':
        snake.change_direction('d')
    if keys[pygame.K_s] and snake.direction.name != 'W':
        snake.change_direction('s')
    if keys[pygame.K_a] and snake.direction.name != 'D':
        snake.change_direction('a')

def main():

    snake = Snake(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE)

    fruits = 0
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_movement_keys(snake)

        snake.move()

        if not fruits:
            fruits += 1
            fruit = Fruit(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE)

        if not snake.check_bounds():
            break
 
        draw_screen(snake, fruit, score)

        if snake.check_fruit(fruit):
            fruits -= 1
            score += 1

        clock.tick(8)

    pygame.quit()
    sys.exit()

main()