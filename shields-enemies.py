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
# TNT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt.png'))
TNT_WIDTH, TNT_HEIGHT = (100, 103)
# TNT = pygame.transform.scale(TNT_SPRITE, (100, 103))
# TNT_LIT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt-lit.png'))
# TNT_LIT = pygame.transform.scale(TNT_LIT_SPRITE, (100, 103))
# SHIELD = pygame.draw.rect(WIN, RED, [WIDTH/2-5, flame_y, 10, 10])

# Shield locations
TOP = [WIDTH/2-50, HEIGHT/2-60, 100, 6]
RIGHT = [WIDTH/2+50, HEIGHT/2-50, 5, 100]
BOTTOM = [WIDTH/2-50, HEIGHT/2+50, 100, 6]
LEFT = [WIDTH/2-55, HEIGHT/2-50, 5, 100]

# Movement
VEL = 2

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

class Enemy():

    def __init__(self, window, x, y):
        self.position = 0
        self.x = x
        self.y = y
        self.img = pygame.image.load(os.path.join('assets', 'flame.png'))
        # self.mask = pygame.mask.from_surface(self.img)
        self.arrows = []

    def shoot(self):
        arrow = Arrow(self.x, self.y, self.img)
        self.arrows.append(arrow)

    def draw(self, window):
        for arrow in self.arrows:
            arrow.draw(window)

    def move_arrow(self, obj):
        for arrow in self.arrows:
            arrow.move()
            if arrow.collision(obj):
                self.arrows.remove(arrow)
                raise SystemExit

class Arrow():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self):
        self.x += VEL

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(obj, self)

# Determine if two objects collide
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

    # def colide(self, other_obj):
    #     print(other_obj.shields[3].blocking)
    #     if not other_obj.shields[3].blocking and self.rect.colliderect(other_obj):
    #         print("crash!")
    #         raise SystemExit
    #     if other_obj.shields[3].blocking and other_obj.shields[3].shield.colliderect(self.rect):
    #         print("blocked!")
    #         self.rect = None


class Player():

    COOLDOWN = 30
    RELOAD_TIME = 12

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.health = 100
        self.block_cooldown = 0
        self.blocking = False
        self.block_reload = 0
        self.can_reload = True
        self.TNT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt.png'))
        self.TNT_WIDTH, self.TNT_HEIGHT = (100, 103)
        self.TNT = pygame.transform.scale(self.TNT_SPRITE, (100, 103))
        self.mask = pygame.mask.from_surface(self.TNT)
        self.rect = self.TNT_SPRITE.get_rect()
        self.TNT_LIT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt-lit.png'))
        self.TNT_LIT = pygame.transform.scale(self.TNT_LIT_SPRITE, (100, 103))

        self.rect.x = self.x - self.TNT_WIDTH/2
        self.rect.y = self.y - self.TNT_HEIGHT/2
        self.top_shield = Shield(TOP) 
        self.right_shield = Shield(RIGHT) 
        self.bottom_shield = Shield(BOTTOM) 
        self.left_shield = Shield(LEFT) 
        self.shields = [self.top_shield, self.right_shield, self.bottom_shield, self.left_shield]

    def draw(self, window):
        self.cooldown()
        self.reload_timer()
        if self.blocking:
            window.blit(self.TNT_LIT, (WIDTH/2-50, HEIGHT/2-54))
        else:
            window.blit(self.TNT, (WIDTH/2-50, HEIGHT/2-54))

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
    pygame.time.delay(2000)
    raise SystemExit

def handle_input(key_pressed, shields, enemy):
    if key_pressed[pygame.K_UP]:
        shields[0].block()
    if key_pressed[pygame.K_RIGHT]:
        shields[1].block()
    if key_pressed[pygame.K_DOWN]:
        shields[2].block()
    if key_pressed[pygame.K_LEFT]:
        shields[3].block()

    if key_pressed[pygame.K_SPACE]:
        enemy.shoot()

def main():

    clock = pygame.time.Clock()

    # Create shields objects
    player = Player(WIDTH/2, HEIGHT/2)
    # top_shield = Shield(TOP)
    # right_shield = Shield(RIGHT)
    # bottom_shield = Shield(BOTTOM)
    # left_shield = Shield(LEFT)
    # shields = [top_shield, right_shield, bottom_shield, left_shield]

    enemy = Enemy(WIN, 0, HEIGHT/2-10)

    def drawWindow():
        WIN.fill(WHITE)
        scoreText = pygame.font.Font('freesansbold.ttf', 70)
        scoreSurface = scoreText.render(str(player.score), True, BLACK)
        WIN.blit(scoreSurface, (20, 20))

        player.draw(WIN)
        for shield in player.shields:
            shield.draw(WIN)
        enemy.draw(WIN)
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

        # enemy.move()
        # player.colide(enemy)

        enemy.move_arrow(player)

        player.draw(WIN)
        handle_input(key_pressed, player.shields, enemy)

    pygame.QUIT()

if __name__ == "__main__":
    main()