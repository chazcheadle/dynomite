#!/usr/bin/python3

import pygame
import os

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

# Movement
VEL = 5

block = False

def flame(flame_y, outside=(255,255,0), inside=(255,0,0)):
    pygame.draw.rect(WIN, outside, [WIDTH/2-5, flame_y, 10, 10])
    pygame.draw.rect(WIN, inside, [WIDTH/2-5+2, flame_y+2, 6, 6])

def drawWindow(tnt, flame_y, block, score):
    scoreText = pygame.font.Font('freesansbold.ttf', 70)
    scoreSurface = scoreText.render(str(score), True, BLACK)
    # scoreRect = scoreSurface.get_rect()
    # scoreRect.center = (WIDTH/2), (HEIGHT/2)

    WIN.fill(WHITE)
    WIN.blit(scoreSurface, (20, 20))

    WIN.blit(TNT, (tnt.x, tnt.y))
    if block:
        flame(flame_y, GRAY, BLACK)
        snip(flame_y, tnt, score)
    else:
        flame(flame_y)

    # if not block and flame_y >= tnt.y-5:
    if not block and flame_y >= tnt.y:
        print("boom")
        boom(tnt)

    pygame.display.update()

def snip(flame_y, tnt, score):
    flame(flame_y, BLACK, GRAY)
    pygame.display.update()
    pygame.time.delay(30)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-5, BLACK, GRAY)
    pygame.display.update()
    pygame.time.delay(30)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-8, BLACK, GRAY)
    pygame.display.update()
    pygame.time.delay(30)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-10, BLACK, GRAY)
    pygame.display.update()
    pygame.time.delay(30)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-8, BLACK, GRAY)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-5, BLACK, GRAY)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-3, GRAY, GRAY)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y-1, LIGHTGRAY, GRAY)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    flame(flame_y, LIGHTGRAY, LIGHTGRAY)
    pygame.display.update()
    pygame.time.delay(50)
    WIN.fill(WHITE)
    pygame.display.update()
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    textSurface = largeText.render(F"You scored: {score}!", True, BLACK)
    textRect = textSurface.get_rect()
    textRect.center = (WIDTH/2), (HEIGHT/2)
    WIN.blit(textSurface, textRect)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.QUIT()

def boom(tnt):
    WIN.fill(RED)
    TNT.fill((0, 0, 200), special_flags=pygame.BLEND_RGB_ADD)
    WIN.blit(TNT, (tnt.x-5, tnt.y))
    pygame.display.update()
    pygame.time.delay(100)
    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x+5, tnt.y))
    TNT.fill((0, 200, 0), special_flags=pygame.BLEND_RGB_ADD)
    pygame.display.update()
    pygame.time.delay(100)
    WIN.fill(BLACK)
    WIN.blit(TNT, (tnt.x, tnt.y))
    TNT.fill((200, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
    pygame.display.update()
    pygame.time.delay(100)
    WIN.fill(RED)
    WIN.blit(TNT, (tnt.x, tnt.y))
    TNT.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
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
    pygame.QUIT()

def tnt_handle_movement(key_pressed, tnt, last_time):
    global block

    if key_pressed[pygame.K_SPACE]:
        # print(F"{pygame.time.get_ticks()}")
        # print("Blocking for 1 sec")
        TNT.fill((0, 0, 200), special_flags=pygame.BLEND_RGB_ADD)
        last_time = pygame.time.get_ticks()
        block = True



def main():

    tnt = pygame.Rect(WIDTH/2 - TNT_WIDTH/2, HEIGHT/2-TNT_HEIGHT/2, TNT_WIDTH, TNT_HEIGHT)

    clock = pygame.time.Clock()

    flame_x = WIDTH/2
    flame_y = 1

    score = 0

    # TNT behavior
    global block
    last_time = 0

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]:
            pygame.QUIT()

        now = pygame.time.get_ticks()
        # if now - last_time >= 2000:
        #     print(F"{now} - {last_time}")
        #     print("blocking ended")
        #     TNT.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_SUB)
        #     block = False
        # else:
        #     block = True
        tnt_handle_movement(key_pressed, tnt, last_time)
        # print(F"blocking: {block}")

        drawWindow(tnt,flame_y, block, score)
        score = int(10 * flame_y)

        # flame(flame_y)
        flame_y = flame_y * 1.02

    pygame.QUIT()

if __name__ == "__main__":
    main()