import pygame
import random
import math
import os
import platform
import pwd
import sys
import datetime
import numpy as np


def pr_provenance():
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("user id:", pwd.getpwuid(os.getuid()).pw_name)
    print("platform info:")
    print("    platform: ", platform.platform())
    print("    uname:    ", platform.uname())
    print("version info:")
    print("    python:   %s" % sys.version)
    print("    numpy:   ", np.__version__)
    print("    pygame:  ", pygame.__version__)
    return


pr_provenance()

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Ball properties
BALL_RADIUS = 20
BALL_COLOR = (255, 255, 255)
COLLISION_COLOR = (255, 0, 0)

# Pool table properties
TABLE_WIDTH, TABLE_HEIGHT = WIDTH, HEIGHT
TABLE_COLOR = (0, 128, 0)


class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = BALL_COLOR

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Collision with walls
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > TABLE_WIDTH:
            self.vx *= -1
        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > TABLE_HEIGHT:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)


def check_collision(ball1, ball2):
    distance = math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
    if distance < 2 * BALL_RADIUS:
        return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball1 = Ball(WIDTH / 2, HEIGHT / 2, 0, 0)
    ball2 = Ball(100, 100, 5, 5)

    running = True
    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(TABLE_COLOR)

        ball1.update()
        ball2.update()

        # Check for collision between balls
        if check_collision(ball1, ball2):
            ball1.color = COLLISION_COLOR
            ball2.color = COLLISION_COLOR
            print("Collision detected!")

        ball1.draw(screen)
        ball2.draw(screen)

        # Target another collision within 10 seconds
        current_time = pygame.time.get_ticks()
        if current_time - start_time > 10000:
            print("Time's up!")
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
