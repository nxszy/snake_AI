import pygame
import sys
from snake import Snake, SnakeFragment, Direction
from fruit import Fruit

pygame.init()

# CONST VALUES
SCREEN_WIDTH = 400
SCREEN_WIDTH_SQUARES = SCREEN_WIDTH // 40
SCREEN_HEIGHT = 440
SCREEN_HEIGHT_SQUARES = SCREEN_HEIGHT // 40
SQUARE_SIZE = 40
GREEN = (38, 173, 40)
LIGHT_GREEN = (100, 250, 102)
GRAY = (116, 128, 119)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 36)


class SnakeAI(Snake):
    
    def check_collision(self, pos_x, pos_y):
        
        if not pos_x:
            head_x, head_y = self.body[0].pos
        else:
            head_x, head_y = pos_x, pos_y

        if not (1 <= head_x <= self.board_max_width) or not (0 <= head_y <= self.board_max_height - 1):
            return False
        
        body_positions = set([fragment.pos for fragment in self.body[1:]])
        if (head_x, head_y) in body_positions:
            return False

        return True 

class gameAI:
    def __init__(self):

        self.snake = SnakeAI(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE)
        self.fruits = 0
        self.score = 0

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.fruit = Fruit(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE, self.snake.body)
        self.reset()

    def reset(self):
        # init game state
        self.snake.direction = Direction.W

        self.snake = SnakeAI(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE)

        self.score = 0
        self.fruit = Fruit(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE, self.snake.body)
        self.frame_iteration = 0


    def move(self, snake, move):
        if move[0] and snake.direction.name != 'S':
            snake.change_direction('w')
        if move[1] and snake.direction.name != 'D':
            snake.change_direction('a')
        if move[2] and snake.direction.name != 'W':
            snake.change_direction('s')
        if move[3] and snake.direction.name != 'A':
            snake.change_direction('d')

    def draw_screen(self, snake, fruit, score):

        self.screen.fill(LIGHT_GREEN)

        for row in range(SCREEN_HEIGHT_SQUARES):
            for col in range(SCREEN_WIDTH_SQUARES):
                if (row == 0):
                    color = GRAY
                elif (row + col) % 2 == 0:
                    color = GREEN
                else:
                    color = LIGHT_GREEN

                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        text = font.render(f"Score: {score}", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, 20)

        self.screen.blit(text, text_rect)

        if fruit:
            fruit.draw(self.screen)

        snake.draw(self.screen)

        pygame.display.flip()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move(self.snake, action)

        self.snake.move()

        if not self.fruits:
            self.fruits += 1
            self.fruit = Fruit(SCREEN_HEIGHT_SQUARES-1, SCREEN_WIDTH_SQUARES, SQUARE_SIZE, self.snake.body)

        reward = 0
        game_over = False
        if not self.snake.check_collision(None, None) or self.frame_iteration > 100*len(self.snake.body):
            game_over = True
            reward -= 10
            return reward, game_over, self.score

        if self.snake.check_fruit(self.fruit):
            self.fruits -= 1
            self.score += 1
            reward += 10

        self.draw_screen(self.snake, self.fruit, self.score)

        self.clock.tick(24)

        return reward, game_over, self.score

'''
if __name__ == '__main__':
    game = gameAI()

    while True:
        game_over, record = game.play_step()

        if game_over:
            break
    
    print(record)
'''