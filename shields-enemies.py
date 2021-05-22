#!/usr/bin/python3

import pygame
import random
import os

from pygame.constants import NOEVENT
from pygame.mixer import fadeout

pygame.init()

# Constants
WIDTH, HEIGHT = 900, 900
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dyno-mite!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHTGRAY = (200, 200, 200)

TNT_WIDTH, TNT_HEIGHT = (100, 103)

# Shield locations
TOP = [WIDTH/2-50, HEIGHT/2-60, 100, 6]
RIGHT = [WIDTH/2+50, HEIGHT/2-50, 5, 100]
BOTTOM = [WIDTH/2-50, HEIGHT/2+50, 100, 6]
LEFT = [WIDTH/2-55, HEIGHT/2-50, 5, 100]

# Movement
VEL = 5

block = False

class Shield():
    COOLDOWN = 20
    RELOAD_TIME = 5

    def __init__(self, name):
        self.name = name
        self.block_cooldown = 0
        self.blocking = False
        self.block_reload = 0
        self.can_reload = True

        # Top
        if name == 'top':
            self.shield = pygame.Surface((100, 6)).convert_alpha()
            pygame.draw.polygon(self.shield,(0,255,0),[(0,0),(100,0),(100,6),(0,6)])
            self.rect = self.shield.get_rect(topleft=(WIDTH/2-50,HEIGHT/2-56))

        # Right
        if name == 'right':
            self.shield = pygame.Surface((6, 100)).convert_alpha()
            pygame.draw.polygon(self.shield,(0,255,0),[(0,0),(6,0),(6,100),(0,100)])
            self.rect = self.shield.get_rect(topleft=(WIDTH/2+44,HEIGHT/2-50))

        # Bottom
        if name == 'bottom':
            self.shield = pygame.Surface((100, 6)).convert_alpha()
            pygame.draw.polygon(self.shield,(0,255,0),[(0,0),(100,0),(100,6),(0,6)])
            self.rect = self.shield.get_rect(topleft=(WIDTH/2-50,HEIGHT/2+50))

        # Left
        if name == 'left':
            self.shield = pygame.Surface((6, 100)).convert_alpha()
            pygame.draw.polygon(self.shield,(0,255,0),[(0,0),(6,0),(6,100),(0,100)])
            self.rect = self.shield.get_rect(topleft=(WIDTH/2-50,HEIGHT/2-50))

        self.mask = pygame.mask.from_surface(self.shield)

    def draw(self, window):
        self.cooldown()
        self.reload_timer()
        if self.blocking:
            window.blit(self.shield, self.rect)

    def cooldown(self):
        if self.block_cooldown >= self.COOLDOWN:
            self.block_cooldown = 0
            self.block_reload += 1
            self.reload_timer()
            self.blocking = False
        elif self.block_cooldown > 0:
            self.block_cooldown += 1
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
            self.blocking = True
            self.block_cooldown += 1

class Enemy():

    RELOAD_TIME = 20

    def __init__(self):
        self.position = 0
        self.img = pygame.image.load(os.path.join('assets', 'flame.png'))
        self.arrows = []
        self.reload_countdown = 0

    def shoot(self, name):
        if self.reload_countdown == 0:
            arrow = Arrow(self.img, name)
            self.arrows.append(arrow)
            self.reload_countdown = 1

    def shoot_random(self):
        if self.reload_countdown == 0:
            arrow = Arrow(self.img, random.choice(['top', 'right', 'bottom', 'left']))
            self.arrows.append(arrow)
            self.reload_countdown = 1

    def draw(self, window):
        for arrow in self.arrows:
            arrow.draw(window)

    def move_arrow(self, obj):
        self.reload_timer()
        for arrow in self.arrows:
            arrow.move()
            for shield in obj.shields:
                if shield.name == arrow.name:
                    if arrow.collision(shield) and shield.blocking:
                        self.arrows.remove(arrow)
                        obj.score += 10

            if arrow.collision(obj):
                self.arrows.remove(arrow)
                obj.health -= 5

    def reload_timer(self):
        if self.reload_countdown >= self.RELOAD_TIME:
            self.reload_countdown = 0
        if self.reload_countdown > 0:
            self.reload_countdown +=1
class Arrow():
    def __init__(self, img, name):

        self.name = name
        self.img = img
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 5

        if name == 'top':        
            self.x = WIDTH/2 - 10
            self.y = 0
            self.vel = 5
        elif name == 'right':
            self.x = WIDTH
            self.y = HEIGHT/2 - 20
            self.vel = -5
        elif name == 'bottom':
            self.x = WIDTH/2 - 20
            self.y = HEIGHT
            self.vel = -5
        elif name == 'left':
            self.x = 0
            self.y = HEIGHT/2 -20
            self.vel = 5

    def move(self):
        if self.name == 'top' or self.name == 'bottom':
            self.y += self.vel
        elif self.name == 'right' or self.name == 'left':
            self.x += self.vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)

# Determine if two objects collide
def collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.x
    offset_y = obj2.rect.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

class Player():

    COOLDOWN = 10
    RELOAD_TIME = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.health = 100
        self.block_cooldown = 0
        self.blocking = False
        self.block_reload = 0
        self.can_reload = True
        self.TNT = pygame.image.load(os.path.join('assets', 'tnt.png'))
        self.TNT_WIDTH, self.TNT_HEIGHT = (100, 103)
        self.mask = pygame.mask.from_surface(self.TNT)
        self.rect = self.TNT.get_rect()
        self.TNT_LIT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt-lit.png'))
        self.TNT_LIT = pygame.transform.scale(self.TNT_LIT_SPRITE, (100, 103))

        self.rect.x = self.x - self.TNT_WIDTH/2
        self.rect.y = self.y - self.TNT_HEIGHT/2
        self.top_shield = Shield('top')
        self.right_shield = Shield('right')
        self.bottom_shield = Shield('bottom')
        self.left_shield = Shield('left')
        self.shields = [self.top_shield, self.right_shield, self.bottom_shield, self.left_shield]

    def draw(self, window):
        self.cooldown()
        self.reload_timer()
        if self.blocking:
            window.blit(self.TNT_LIT, (self.x, self.y))
        else:
            window.blit(self.TNT, (self.x, self.y))

    def cooldown(self):
        if self.block_cooldown >= self.COOLDOWN:
            self.block_cooldown = 0
            self.block_reload += 1
            self.reload_timer()
            self.blocking = False
        elif self.block_cooldown > 0:
            self.block_cooldown += 1
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

    def colide(self, other_obj):
        if not self.shields[3].blocking and other_obj.rect.colliderect(self.rect):
            boom(self.TNT, self.score)
        if self.shields[3].blocking and other_obj.rect.colliderect(self.rect):
            self.score += 10
            other_obj.rect.x = 0

def boom(tnt, score):
    WIN.fill(RED)
    tnt.fill((0, 0, 200), special_flags=pygame.BLEND_RGB_ADD)
    WIN.blit(tnt, (WIDTH/2-50, HEIGHT/2-54))
    pygame.display.update()
    pygame.time.delay(100)
    WIN.fill(WHITE)
    WIN.blit(tnt, (WIDTH/2-50, HEIGHT/2-54))
    tnt.fill((0, 200, 0), special_flags=pygame.BLEND_RGB_ADD)
    pygame.display.update()
    pygame.time.delay(100)
    WIN.fill(BLACK)
    WIN.blit(tnt, (WIDTH/2-50, HEIGHT/2-54))
    tnt.fill((200, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
    pygame.display.update()
    pygame.time.delay(100)
    WIN.fill(RED)
    WIN.blit(tnt, (WIDTH/2-50, HEIGHT/2-54))
    tnt.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(RED)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    pygame.display.update()
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    textSurface = largeText.render("Boom!", True, BLACK)
    textRect = textSurface.get_rect()
    textRect.center = (WIDTH/2), (HEIGHT/2)
    WIN.blit(textSurface, textRect)
    pygame.display.update()
    pygame.time.delay(2000)
    WIN.fill(WHITE)
    pygame.display.update()
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    textSurface = largeText.render(F"You scored: {score}!", True, BLACK)
    textRect = textSurface.get_rect()
    textRect.center = (WIDTH/2), (HEIGHT/2)
    WIN.blit(textSurface, textRect)
    pygame.display.update()
    pygame.time.delay(3000)


def handle_input(key_pressed, player, enemy, run):
    if key_pressed[pygame.K_UP]:
        player.top_shield.block()
    if key_pressed[pygame.K_RIGHT]:
        player.right_shield.block()
    if key_pressed[pygame.K_DOWN]:
        player.bottom_shield.block()
    if key_pressed[pygame.K_LEFT]:
        player.left_shield.block()

    if run == False and key_pressed[pygame.K_SPACE]:
        run = True

def main():

    clock = pygame.time.Clock()

    player = Player(WIDTH/2-50, HEIGHT/2-54)

    enemy = Enemy()

    def drawWindow():
        WIN.fill(WHITE)
        scoreText = pygame.font.Font('freesansbold.ttf', 50)
        scoreSurface = scoreText.render(F"Score: {str(player.score)}", True, BLACK)
        WIN.blit(scoreSurface, (20, 20))

        healthText = pygame.font.Font('freesansbold.ttf', 50)
        healthSurface = healthText.render(F"health: {str(player.health)}", True, BLACK)
        WIN.blit(healthSurface, (WIDTH/2, 20))

        player.draw(WIN)
        for shield in player.shields:
            shield.draw(WIN)
        enemy.draw(WIN)
        pygame.display.update()

    FIRE_ARROW, t, trail = pygame.USEREVENT+1, 500, []
    pygame.time.set_timer(FIRE_ARROW, t)

    run = True
    while run:
        clock.tick(FPS)
        drawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == FIRE_ARROW:
                enemy.shoot_random()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]:
            pygame.QUIT

        enemy.move_arrow(player)

        player.draw(WIN)
        handle_input(key_pressed, player, enemy, run)

        if player.health <= 0:
            run = False
            boom(player.TNT, player.score)

    pygame.QUIT

if __name__ == "__main__":
    main()