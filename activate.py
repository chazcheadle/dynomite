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
TNT_LIT_SPRITE = pygame.image.load(os.path.join('assets', 'tnt-lit.png'))
TNT_LIT = pygame.transform.scale(TNT_LIT_SPRITE, (100, 103))

# Movement
VEL = 5

block = False

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

def handle_input(key_pressed, player):
    # if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
    #     if tnt.x > 0:
    #         tnt.x -= VEL
    if key_pressed[pygame.K_SPACE]:
        player.block()

        # if tnt.y > 0:
        #     tnt.y -= VEL
    # if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
    #     if tnt.x + 103 <= WIDTH:
    #         tnt.x += VEL
    # if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
    #     if tnt.y + 104 <= HEIGHT:
    #         tnt.y += VEL



def main():

    clock = pygame.time.Clock()


    player = Player()

    def drawWindow():
        WIN.fill(WHITE)
        player.draw(WIN)
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

        player.draw(WIN)
        handle_input(key_pressed, player)



    pygame.QUIT()

if __name__ == "__main__":
    main()


        # now = pygame.time.get_ticks()
        # if now - last_time >= 2000:
        #     print(F"{now} - {last_time}")
        #     print("blocking ended")
        #     TNT.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_SUB)
        #     block = False
        # else:
        #     block = True
        # tnt_handle_movement(key_pressed, tnt, last_time)
        # print(F"blocking: {block}")

        # flame(flame_y)
        # flame_y = flame_y * 1.02



# def snip(flame_y, tnt):
#     flame(flame_y, BLACK, GRAY)
#     pygame.display.update()
#     pygame.time.delay(30)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-5, BLACK, GRAY)
#     pygame.display.update()
#     pygame.time.delay(30)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-8, BLACK, GRAY)
#     pygame.display.update()
#     pygame.time.delay(30)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-10, BLACK, GRAY)
#     pygame.display.update()
#     pygame.time.delay(30)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-8, BLACK, GRAY)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-5, BLACK, GRAY)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-3, GRAY, GRAY)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y-1, LIGHTGRAY, GRAY)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     flame(flame_y, LIGHTGRAY, LIGHTGRAY)
#     pygame.display.update()
#     pygame.time.delay(50)


#     WIN.fill(WHITE)
#     pygame.display.update()
#     largeText = pygame.font.Font('freesansbold.ttf', 100)
#     textSurface = largeText.render("You Win!", True, BLACK)
#     textRect = textSurface.get_rect()
#     textRect.center = (WIDTH/2), (HEIGHT/2)
#     WIN.blit(textSurface, textRect)
#     pygame.display.update()
#     pygame.time.delay(2000)
#     pygame.QUIT()

# def boom(tnt):
#     WIN.fill(RED)
#     TNT.fill((0, 0, 200), special_flags=pygame.BLEND_RGB_ADD)
#     WIN.blit(TNT, (tnt.x-5, tnt.y))
#     pygame.display.update()
#     pygame.time.delay(100)
#     WIN.fill(WHITE)
#     WIN.blit(TNT, (tnt.x+5, tnt.y))
#     TNT.fill((0, 200, 0), special_flags=pygame.BLEND_RGB_ADD)
#     pygame.display.update()
#     pygame.time.delay(100)
#     WIN.fill(BLACK)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     TNT.fill((200, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
#     pygame.display.update()
#     pygame.time.delay(100)
#     WIN.fill(RED)
#     WIN.blit(TNT, (tnt.x, tnt.y))
#     TNT.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(WHITE)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(RED)
#     pygame.display.update()
#     pygame.time.delay(50)
#     WIN.fill(WHITE)
#     pygame.display.update()

#     largeText = pygame.font.Font('freesansbold.ttf', 100)
#     textSurface = largeText.render("Boom!", True, BLACK)
#     textRect = textSurface.get_rect()
#     textRect.center = (WIDTH/2), (HEIGHT/2)
#     WIN.blit(textSurface, textRect)
#     pygame.display.update()
#     pygame.time.delay(2000)
#     pygame.QUIT()
