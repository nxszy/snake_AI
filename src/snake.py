import pygame
from enum import Enum
from typing import List

BODY_BOTTOMLEFT = pygame.image.load('./assets/body_bottomleft.png')
BODY_BOTTOMRIGHT = pygame.image.load('./assets/body_bottomright.png')
BODY_HORIZONTAL = pygame.image.load('./assets/body_horizontal.png')
BODY_TOPLEFT = pygame.image.load('./assets/body_topleft.png')
BODY_TOPRIGHT = pygame.image.load('./assets/body_topright.png')
BODY_VERTICAL = pygame.image.load('./assets/body_vertical.png')
HEAD_DOWN = pygame.image.load('./assets/head_down.png')
HEAD_LEFT = pygame.image.load('./assets/head_left.png')
HEAD_RIGHT = pygame.image.load('./assets/head_right.png')
HEAD_UP = pygame.image.load('./assets/head_up.png')
TAIL_DOWN = pygame.image.load('./assets/tail_down.png')
TAIL_LEFT = pygame.image.load('./assets/tail_left.png')
TAIL_RIGHT = pygame.image.load('./assets/tail_right.png')
TAIL_UP = pygame.image.load('./assets/tail_up.png')

class Direction(Enum):
    W = (-1,0)
    A = (0,-1)
    S = (1,0)
    D = (0,1)

class SnakeFragment():
    def __init__(self, x: int, y: int, direction: Direction = 'W', image = None) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image

    @property
    def pos(self):
        return (self.x, self.y)
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, new_direction):
        self._direction = new_direction

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image

class Snake():
    
    def __init__(self, board_max_width: int, board_max_height: int, square_size: int) -> None:

        default_head = SnakeFragment(board_max_width//2, board_max_height//2, 'W', HEAD_UP)
        default_body1 = SnakeFragment(board_max_width//2+1, board_max_height//2, 'W', BODY_VERTICAL)
        default_body2 = SnakeFragment(board_max_width//2+2, board_max_height//2, 'W', BODY_VERTICAL)
        default_body3 = SnakeFragment(board_max_width//2+3, board_max_height//2, 'W', BODY_VERTICAL)
        default_body4 = SnakeFragment(board_max_width//2+4, board_max_height//2, 'W', BODY_VERTICAL)
        default_tail = SnakeFragment(board_max_width//2+5, board_max_height//2, 'W', TAIL_UP)

        self.body = [default_head, default_body1, default_body2, default_body3, default_body4, default_tail]
        self.board_max_width = board_max_width
        self.board_max_height = board_max_height
        self.square_size = square_size
        self.direction = Direction.W

    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, new_body):
        self._body = new_body

    def change_direction(self, move):
        
        match move:
            case 'w':
                self.direction = Direction.W
            case 'a':
                self.direction = Direction.A
            case 's':
                self.direction = Direction.S
            case 'd':
                self.direction = Direction.D

    def move(self):

        move_x, move_y = self.direction.value
        head_x, head_y = self.body[0].pos

        new_head = SnakeFragment(head_x + move_x, head_y + move_y, self.direction, self.get_image('head', self.direction))
        new_body = [new_head]
        
        for i in range(0, len(self.body)-1):
            new_fragment = self.body[i]
            new_fragment.direction = new_body[i-1].direction
            new_body.append(self.body[i])

        for i in range(1, len(new_body)-1):
            new_body[i].image = self.get_image('body', new_body[i-1].pos, new_body[i].pos, new_body[i+1].pos)

        new_body[-1].image = self.get_image('tail', new_body[-2].pos, new_body[-1].pos)

        self.body = new_body

    def get_image(self, type: str, *directions):
        
        match type:

            case 'head':
                dir = directions[0].name
                match dir:
                    case 'W':
                        return HEAD_UP
                    case 'A':
                        return HEAD_LEFT
                    case 'S':
                        return HEAD_DOWN
                    case 'D':
                        return HEAD_RIGHT
                    
            case 'body':
                previous, current, next = directions[0], directions[1], directions[2]
                if previous[0] - current[0] == 1 and next[1] - current[1] == 1:
                    return BODY_BOTTOMRIGHT
                if current[0] - previous[0] == 1 and next[1] - current[1] == 1:
                    return BODY_TOPRIGHT
                if current[1] - previous[1] == 1 and next[0] - current[0] == 1:
                    return BODY_BOTTOMLEFT
                if current[0] - previous[0] == 1 and current[1] - next[1] == 1:
                    return BODY_TOPLEFT
                if previous[1] == current[1] == next[1]:
                    return BODY_VERTICAL
                else:
                    return BODY_HORIZONTAL
                
            case 'tail':
                previous, tail = directions[0], directions[1]
                if tail[0] - previous[0] == 1:
                    return TAIL_DOWN
                if previous[0] - tail[0] == 1:
                    return TAIL_UP
                if tail[1] - previous[1] == 1:
                    return TAIL_RIGHT
                else:
                    return TAIL_LEFT

    def check(self):
        
        head_x, head_y = self.body[0].pos

        if not ((0 < head_x <= self.board_max_width) and (0 < head_y <= self.board_max_height)):
            return False
        
        if (head_x, head_y) in self.body:
            return False

        return True
    
    def draw(self, screen: pygame.display):
        for fragment in self.body:
            frag_x, frag_y = fragment.pos
            screen.blit(fragment.image, ((frag_y-1)*self.square_size, (frag_x-1)*self.square_size))
            