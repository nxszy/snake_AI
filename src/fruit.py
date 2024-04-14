import pygame
import random

APPLE = pygame.image.load('./assets/apple.png')

class Fruit:
    def __init__(self, board_max_width: int, board_max_height: int, square_size: int, snake_body):

        self.board_max_width = board_max_width
        self.board_max_height = board_max_height
        self.square_size = square_size

        self.image = APPLE
        self.snake_body = snake_body

        self.x, self.y = self.generate_position()

    @property
    def pos(self):
        return (self.x, self.y)
    
    def generate_position(self):
        free_squares = [(x, y) for x in range(1, self.board_max_width) for y in range(self.board_max_height) if (x,y) not in [frag.pos for frag in self.snake_body]]
        return random.choice(free_squares)

    def draw(self, screen: pygame.display):
        screen.blit(self.image, (self.y*self.square_size, self.x*self.square_size))