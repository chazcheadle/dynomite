#!/usr/bin/python3

import pygame
import random
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
VEL = 5

block = False

class Shield():
    COOLDOWN = 20
    RELOAD_TIME = 10

    def __init__(self, position):
        self.position = None

        self.shield = pygame.Surface((6, 100)).convert_alpha()
        self.shield.fill(RED)
        pygame.draw.polygon(self.shield,(0,255,0),[(0,0),(6,0),(6,100),(0,100)])
        self.rect = self.shield.get_rect(topleft=(WIDTH/2-50,HEIGHT/2-50))
        self.mask = pygame.mask.from_surface(self.shield)

        self.block_cooldown = 0
        self.blocking = False
        self.block_reload = 0
        self.can_reload = True

    def draw(self, window):
        self.cooldown()
        self.reload_timer()
        if self.blocking:
            window.blit(self.shield, self.rect)
            # pygame.draw.rect(window, RED, self.shield)

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
            print("blocking")
            self.block_cooldown += 1

class Enemy():

    RELOAD_TIME = 20

    def __init__(self):
        self.position = 0
        self.img = pygame.image.load(os.path.join('assets', 'flame.png'))
        # self.mask = pygame.mask.from_surface(self.img)
        self.arrows = []
        self.reload_countdown = 0

    def shoot(self, position):
        if self.reload_countdown == 0:
            arrow = Arrow(self.img, position)
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
            if arrow.collision(obj.shields[3]) and obj.shields[3].blocking:
                print('BLOCKED')
                self.arrows.remove(arrow)
                obj.score += 10
            elif arrow.collision(obj):
                self.arrows.remove(arrow)
                obj.health -= 5
                # raise SystemExit

    def reload_timer(self):
        if self.reload_countdown >= self.RELOAD_TIME:
            self.reload_countdown = 0
        if self.reload_countdown > 0:
            self.reload_countdown +=1
class Arrow():
    def __init__(self, img, position):

        self.position = position
        self.img = img
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 5

        if position == 'top':        
            self.x = WIDTH/2 - 10
            self.y = 0
            self.vel = 5
        elif position == 'right':
            self.x = WIDTH
            self.y = HEIGHT/2 - 20
            self.vel = -5
        elif position == 'bottom':
            self.x = WIDTH/2 - 20
            self.y = HEIGHT
            self.vel = -5
        elif position == 'left':
            self.x = 0
            self.y = HEIGHT/2 -20
            self.vel = 5

    def move(self):
        if self.position == 'top' or self.position == 'bottom':
            self.y += self.vel
        elif self.position == 'right' or self.position == 'left':
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

    # def colide(self, other_obj):
    #     print(other_obj.shields[3].blocking)
    #     if not other_obj.shields[3].blocking and self.rect.colliderect(other_obj):
    #         print("crash!")
    #         raise SystemExit
    #     if other_obj.shields[3].blocking and other_obj.shields[3].shield.colliderect(self.rect):
    #         print("blocked!")
    #         self.rect = None


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
        # self.TNT = pygame.transform.scale(self.TNT_SPRITE, (100, 103))
        self.mask = pygame.mask.from_surface(self.TNT)
        self.rect = self.TNT.get_rect()
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
        # print(self.health)
        self.cooldown()
        self.reload_timer()
        if self.blocking:
            window.blit(self.TNT_LIT, (self.x, self.y))
        else:
            window.blit(self.TNT, (self.x, self.y))

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
        # for arrow in other_obj:
        #     print(arrow.rect.x)
        #     if self.shields[3].blocking and self.rect.colliderect(arrow.rect):
        #         self.score += 10
        #         print('blocked')
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
        enemy.shoot_random()

def main():

    clock = pygame.time.Clock()

    # Create shields objects
    player = Player(WIDTH/2-50, HEIGHT/2-54)
    # top_shield = Shield(TOP)
    # right_shield = Shield(RIGHT)
    # bottom_shield = Shield(BOTTOM)
    # left_shield = Shield(LEFT)
    # shields = [top_shield, right_shield, bottom_shield, left_shield]

    enemy = Enemy()

    def drawWindow():
        WIN.fill(WHITE)
        scoreText = pygame.font.Font('freesansbold.ttf', 70)
        scoreSurface = scoreText.render(F"Score: {str(player.score)}", True, BLACK)
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
        # player.colide(enemy.arrows)

        enemy.move_arrow(player)

        player.draw(WIN)
        handle_input(key_pressed, player.shields, enemy)

    pygame.QUIT()

if __name__ == "__main__":
    main()