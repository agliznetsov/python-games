import random
import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))


class PythonGame:
    def __init__(self):
        self.quit = False
        self.direction = ''
        self.apple = (0, 0)
        self.score = 0
        self.delay = 100
        self.snake = []
        self.reset(3)

    def reset(self, length):
        self.direction = 'right'
        self.apple = (random.randint(0, 24), random.randint(0, 24))
        self.score = 0
        self.delay = 100
        self.snake = []
        for x in range(0, length):
            self.snake.insert(0, (x + 5, 5))

    def draw(self):
        win.fill((0, 0, 0))
        pygame.display.set_caption("Score: " + str(self.score))
        pygame.draw.circle(win, (0, 255, 0), (self.apple[0] * 20 + 10, self.apple[1] * 20 + 10), radius=9)
        for i in range(0, len(self.snake)):
            segment = self.snake[i]
            rect = (segment[0] * 20 + 1, segment[1] * 20 + 1, 18, 18)
            if i == 0:
                rect = (segment[0] * 20, segment[1] * 20, 20, 20) #head
            pygame.draw.rect(win, (255, 0, 0), rect)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.quit = True
            return
        if keys[pygame.K_LEFT] and self.direction != 'right':
            self.direction = 'left'
        if keys[pygame.K_RIGHT] and self.direction != 'left':
            self.direction = 'right'
        if keys[pygame.K_UP] and self.direction != 'down':
            self.direction = 'up'
        if keys[pygame.K_DOWN] and self.direction != 'up':
            self.direction = 'down'

    def move(self):
        head = self.snake[0]
        x = head[0]
        y = head[1]
        if self.direction == 'left':
            x -= 1
        if self.direction == 'right':
            x += 1
        if self.direction == 'up':
            y -= 1
        if self.direction == 'down':
            y += 1

        if x > 24:
            x = 0
        if x < 0:
            x = 24
        if y > 24:
            y = 0
        if y < 0:
            y = 24

        head = (x, y)
        for segment in self.snake:
            if segment == head:
                self.reset(3)
                return
        else:
            self.snake.insert(0, head)
            if self.apple == head:
                self.score += 10
                if self.delay > 20:
                    self.delay -= 5
                self.apple = (random.randint(0, 24), random.randint(0, 24))
            else:
                self.snake.pop(len(self.snake) - 1)

    def run(self):
        move_time = 0
        while not self.quit:
            self.handle_events()
            current_time = pygame.time.get_ticks()
            if current_time - move_time > self.delay:
                self.move()
                move_time = current_time
            self.draw()


PythonGame().run()
pygame.quit()
