import random
import pygame
import util

GAME_FPS = 50
DISPLAY_SIZE = (800, 600)
PADDLE_SPEED = 10
BALL_SPEED = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image("arkanoid/ball.png")
        self.rect = self.image.get_rect()
        self.hit_sound = util.load_sound("sound/hit.wav")
        self.punch_sound = util.load_sound("sound/punch.wav")
        self.reset_sound = util.load_sound("sound/cosmic.wav")

    def reset(self, paddle):
        self.vx = BALL_SPEED
        self.vy = -BALL_SPEED
        self.rect.x = paddle.rect.x + paddle.rect.width / 2
        self.rect.y = paddle.rect.y - self.rect.height
        self.reset_sound.play()

    def check_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.vy = -self.vy
            self.punch_sound.play()
        if self.rect.y > DISPLAY_SIZE[1] - self.rect.height:
            self.reset(paddle)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x < 0 or self.rect.x > DISPLAY_SIZE[0] - self.rect.width:
            self.vx = -self.vx
        if self.rect.y < 0:
            self.vy = -self.vy


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image("arkanoid/paddle.png")
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 550
        self.vx = 0

    def update(self):
        if self.vx < 0 and self.rect.x > 0:
            self.rect.x += self.vx
        if self.vx > 0 and self.rect.x < DISPLAY_SIZE[0] - self.rect.width:
            self.rect.x += self.vx

class ArkanoidGame:

    def __init__(self):
        self.quit = False
        self.clock = pygame.time.Clock()
        self.keys = {}
        self.keys[pygame.K_LEFT] = False
        self.keys[pygame.K_RIGHT] = False
        self.background = util.load_image("arkanoid/background.png")
        self.ball = Ball()
        self.paddle = Paddle()
        self.ball.reset(self.paddle)
        self.sprites = [self.ball, self.paddle]
        self.screen = self.create_window()
        self.screen.blit(self.background, (0, 0))

    def create_window(self):
        pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.set_caption("Arkanoid")
        return pygame.display.get_surface()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
                if event.key == pygame.K_ESCAPE:
                    self.quit = True
            if event.type == pygame.KEYUP:
                self.keys[event.key] = False

    def update(self):
        self.paddle.vx = 0
        if (self.keys[pygame.K_LEFT]):
            self.paddle.vx = -PADDLE_SPEED
        if (self.keys[pygame.K_RIGHT]):
            self.paddle.vx = PADDLE_SPEED

        # clear
        for sprite in self.sprites:
            self.screen.blit(self.background, sprite.rect, sprite.rect)

        self.ball.check_paddle(self.paddle)

        # Update and redraw, if visible.
        for sprite in self.sprites:
            sprite.update()
            # if sprite.visible:
            self.screen.blit(sprite.image, sprite.rect)

        pygame.display.update()

    def run(self):
        while not self.quit:
            self.handle_events()
            self.update()
            self.clock.tick(GAME_FPS)


pygame.init()
win = pygame.display.set_mode((500, 500))
ArkanoidGame().run()
pygame.quit()
