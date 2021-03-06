#!/usr/bin/python3

import pygame
import os

from pygame.constants import NOEVENT

pygame.init()

# Constants
WIDTH, HEIGHT = 900, 500
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dyno-mite!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHTGRAY = (200, 200, 200)
# Players
TNT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt.png'))
TNT_WIDTH, TNT_HEIGHT = (100, 103)
TNT = pygame.transform.scale(TNT_SPRITE, (100, 103))
TNT_LIT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt-lit.png'))
TNT_LIT = pygame.transform.scale(TNT_LIT_SPRITE, (100, 103))
# SHIELD = pygame.draw.rect(WIN, RED, [WIDTH/2-5, flame_y, 10, 10])

# Shield locations
TOP = [WIDTH/2-50, HEIGHT/2-60, 100, 6]
RIGHT = [WIDTH/2+50, HEIGHT/2-50, 5, 100]
BOTTOM = [WIDTH/2-50, HEIGHT/2+50, 100, 6]
LEFT = [WIDTH/2-55, HEIGHT/2-50, 5, 100]

# Movement
VEL = 5

block = False


class Shield():
    COOLDOWN = 30
    RELOAD_TIME = 12

    

    def __init__(self, position):
        self.position = None
        self.shield = pygame.draw.rect(WIN, RED, position)
        self.block_cooldown = 0
        self.blocking = False
        self.block_reload = 0
        self.can_reload = True
        

    def draw(self, window):
        self.cooldown()
        self.reload_timer()
        if self.blocking:
            pygame.draw.rect(window, RED, self.shield)


    def cooldown(self):
        if self.block_cooldown >= self.COOLDOWN:
            self.block_cooldown = 0
            # print("cooldown")
            self.block_reload += 1
            self.reload_timer()
            self.blocking = False
        elif self.block_cooldown > 0:
            self.block_cooldown += 1
            # print("hot")
            self.blocking = True
            self.can_reload = False

    def reload_timer(self):
        if self.block_reload >= self.RELOAD_TIME:
            self.block_reload = 0
            self.can_reload = True
        if self.block_reload > 0:
            self.block_reload +=1
            self.can_reload = False

    def block(self):
        if self.can_reload and self.block_cooldown == 0:
            self.block_cooldown += 1

class Player():

    COOLDOWN = 30
    RELOAD_TIME = 12

    def __init__(self):
        self.score = 0
        self.health = 100
        self.mask = pygame.mask.from_surface(TNT)
        self.block_cooldown = 0
        self.blocking = False
        self.block_reload = 0
        self.can_reload = True

    def draw(self, window):
        self.cooldown()
        self.reload_timer()
        print(self.block_cooldown)
        if self.blocking:
            window.blit(TNT_LIT, (WIDTH/2-50, HEIGHT/2-54))
        else:
            window.blit(TNT, (WIDTH/2-50, HEIGHT/2-54))

    def cooldown(self):
        if self.block_cooldown >= self.COOLDOWN:
            self.block_cooldown = 0
            # print("cooldown")
            self.block_reload += 1
            self.reload_timer()
            self.blocking = False
        elif self.block_cooldown > 0:
            self.block_cooldown += 1
            # print("hot")
            self.blocking = True
            self.can_reload = False

    def reload_timer(self):
        if self.block_reload >= self.RELOAD_TIME:
            self.block_reload = 0
            self.can_reload = True
        if self.block_reload > 0:
            self.block_reload +=1
            self.can_reload = False

    def block(self):
        if self.can_reload and self.block_cooldown == 0:
            self.block_cooldown += 1

def handle_input(key_pressed, shields):
    if key_pressed[pygame.K_UP]:
        shields[0].block()
    if key_pressed[pygame.K_RIGHT]:
        shields[1].block()
    if key_pressed[pygame.K_DOWN]:
        shields[2].block()
    if key_pressed[pygame.K_LEFT]:
        shields[3].block()

def main():

    clock = pygame.time.Clock()

    # Create shields objects
    player = Player()
    top_shield = Shield(TOP)
    right_shield = Shield(RIGHT)
    bottom_shield = Shield(BOTTOM)
    left_shield = Shield(LEFT)
    shields = [top_shield, right_shield, bottom_shield, left_shield]

    def drawWindow():
        WIN.fill(WHITE)
        player.draw(WIN)
        for shield in shields:
            shield.draw(WIN)
        pygame.display.update()

    run = True
    while run:
        clock.tick(FPS)
        drawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]:
            pygame.QUIT()

        top_shield.draw(WIN)

        player.draw(WIN)
        handle_input(key_pressed, shields)

    pygame.QUIT()

if __name__ == "__main__":
    main()