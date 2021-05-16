#!/usr/bin/python3

import pygame
import os

# Constants
WIDTH, HEIGHT = 900, 500
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dyno-mite!")

# Colors
WHITE = (255, 255, 255)

# Players
TNT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt.png'))
TNT_WIDTH, TNT_HEIGHT = (100, 103)
TNT = pygame.transform.scale(TNT_SPRITE, (100, 103))

# Movement
VEL = 5

def drawWindow(tnt):

    WIN.fill(WHITE)
    WIN.blit(TNT, (tnt.x, tnt.y))
    pygame.display.update()

def tnt_handle_movement(key_pressed, tnt):
    if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
       if tnt.x > 0:
           tnt.x -= VEL
    if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
        if tnt.y > 0:
            tnt.y -= VEL
    if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
        if tnt.x + 103 <= WIDTH:
            tnt.x += VEL
    if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
        if tnt.y + 104 <= HEIGHT:
            tnt.y += VEL

def main():

    tnt = pygame.Rect(WIDTH/2 - TNT_WIDTH/2, HEIGHT/2-TNT_HEIGHT/2, TNT_WIDTH, TNT_HEIGHT)

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]:
            pygame.QUIT()

        tnt_handle_movement(key_pressed, tnt)
        drawWindow(tnt)



    pygame.QUIT()

if __name__ == "__main__":
    main()