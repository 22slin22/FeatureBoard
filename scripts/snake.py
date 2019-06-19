import pygame
import random

from featureboard.board import Board

pygame.init()

FPS = 3
BOARDS = 3
USE_MONITOR = True


class Game:
    def __init__(self, width, height, led_board):
        self.width = width
        self.height = height
        self.led_board = led_board
        self.running = False
        self.snake = Snake()
        self.food = self.get_random_food_position()

        self.screen = pygame.display.set_mode([self.width * 40, self.height * 40])
        self.screen.fill([255, 255, 255])
        self.clock = pygame.time.Clock()

    def start(self):
        self.running = True
        self.led_board.start_displaying()
        self.run()

    def run(self):
        while self.running:
            self.tick()
            self.draw()
            # one frame per second
            self.clock.tick(FPS)
        self.led_board.matrix.clear()

    def tick(self):
        self.key_inputs()
        self.snake.move()
        if self.snake.check_food_eaten(self.food):
            self.snake.grow = True
            self. food = self.get_random_food_position()
        else:
            self.snake.grow = False

    def draw(self):
        if USE_MONITOR:
            if self.snake.tail_removed is not None:
                pygame.draw.rect(self.screen, [255, 255, 255], [self.snake.tail_removed[1] * 40, self.snake.tail_removed[0] * 40, 40, 40])
            pygame.draw.rect(self.screen, [0, 255, 0], [self.snake.head[1] * 40, self.snake.head[0] * 40, 40, 40])
            pygame.draw.rect(self.screen, [255, 0, 0], [self.food[1] * 40, self.food[0] * 40, 40, 40])
            pygame.display.flip()

        if self.snake.tail_removed is not None:
            self.led_board.matrix.set_led(self.snake.tail_removed[0], self.snake.tail_removed[1], "off")
        self.led_board.matrix.set_led(self.snake.head[0], self.snake.head[1], "green")
        self.led_board.matrix.set_led(self.food[0], self.food[1], "red")

    def get_random_food_position(self):
        """generates random x-y coordinates that are not occupied by the snake body"""
        # create a set of all possible positions
        all_positions = {(y, x) for y in range(self.height) for x in range(self.width)}
        # remove all the positions blocked by the snake
        allowed_positions = all_positions - set(self.snake.body)
        # chose a random one
        return random.choice(list(allowed_positions))

    def check_dead(self):
        # check if snake is out of boundaries
        if self.snake.head[0] < 0 or self.snake.head[0] >= self.height:
            return True
        if self.snake.head[1] < 0 or self.snake.head[1] >= self.width:
            return True
        # check if the head went into the body
        if self.snake.head in self.snake.body[:-1]:
            return True
        return False

    def key_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.direction = Snake.UP
                if event.key == pygame.K_RIGHT:
                    self.snake.direction = Snake.RIGHT
                if event.key == pygame.K_DOWN:
                    self.snake.direction = Snake.DOWN
                if event.key == pygame.K_LEFT:
                    self.snake.direction = Snake.LEFT


class Snake:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self):
        self.head = [0, 0]      # position of the head
        self.tail_removed = None      # keep track of with body part was removed (useful for drawing)
        self.length = 0
        self.grow = False
        self.direction = self.RIGHT
        self.body = [(0, 0)]    # set of position of every body part

    def move(self):
        if self.direction == self.UP:
            self.head[0] -= 1
        if self.direction == self.RIGHT:
            self.head[1] += 1
        if self.direction == self.DOWN:
            self.head[0] += 1
        if self.direction == self.LEFT:
            self.head[1] -= 1
        # add the new head
        self.body.append(tuple(self.head))
        # remove the tail
        if not self.grow:
            self.tail_removed = self.body[0]
            del self.body[0]
        else:
            self.tail_removed = None

    def check_food_eaten(self, food_pos):
        if self.head == list(food_pos):
            return True
        return False


if __name__ == '__main__':
    board = Board(BOARDS)
    game = Game(24, int(BOARDS/3) * 8, board)
    game.start()
