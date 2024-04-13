import pygame
import random

APPLE = pygame.image.load('./assets/apple.png')

class Fruit:
    def __init__(self, board_max_width: int, board_max_height: int, square_size: int):
        self.x = random.randint(0, board_max_width)
        self.y = random.randint(0, board_max_height)
        self.board_max_width = board_max_width
        self.board_max_height = board_max_height
        self.square_size = square_size
        self.image = APPLE

    def draw(self, screen: pygame.display):
        screen.blit(self.image, (self.y*self.square_size, self.x*self.square_size))

    def refresh(self):
        self.x = random.randint(0, self.board_max_width)
        self.y = random.randint(0, self.board_max_height)