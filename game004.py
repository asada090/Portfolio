import pygame
from pygame.locals import *
import sys

def main():
    (w,h) = (400,400)
    (x,y) = (200,200)
    pygame.init()
    pygame.display.set_mode((w,h))
    screen = pygame.display.get_surface()
    
    bg = pygame.image.load("bg.png").convert_alpha()
    rect_bg = bg.get_rect()
    
    player = pygame.image.load("player.png").convert_alpha()
    rect_player = player.get_rect()
    rect_player.center = (x,y)
    
    while(1):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            rect_player.move_ip(-5,0)
        if pressed_key[K_RIGHT]:
            rect_player.move_ip(5,0)
        if pressed_key[K_UP]:
            rect_player.move_ip(0,-5)
        if pressed_key[K_DOWN]:
            rect_player.move_ip(0,5)
        
        pygame.display.update()
        pygame.time.wait(30)
        screen.fill((0,20,0,0))
        screen.blit(bg,rect_bg)
        screen.blit(player,rect_player)
        
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                x,y = event.pos
                x -= int(player.get_width()//2)
                y -= int(player.get_height()//2)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
if __name__ == "__main__":
    main()