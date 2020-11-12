import pygame
from pygame.locals import *
import sys

SCREEN = Rect(0,0,400,400)

class Sprite(pygame.sprite.Sprite):
    def __init__(self,filename,(x,y),(vx,vy),angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        if angle != 0:
            self.image = pygame.transform.rotate(self.image,angle)
        w = self.image.get_width()
        h = self.image.get_height()
        self.rect = Rect(x,y,w,h)
        self.vx = vx
        self.vy = vy
        self.angle = angle
        
    def update(self):
        self.rect.move_ip(self.vx,self.vy)
        if self.rect.left < 0 or self.rect.right > SCREEN.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCREEN.height:
            self.vy = -self.vy
        self.rect = self.rect.clamp(SCREEN)
        
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    player = Sprite("",(200,200),(2,0),0)
    enemy1 = Sprite("",(200,200),(0,2),0)
    enemy2 = Sprite("",(200,200),(2,2),10)
    
    group = pygame.sprite.RenderUpdates()
    
    group.add(player)
    group.add(enemy1)
    group.add(enemy2)
    clock = pygame.time.Clock()
    
    while(1):
        clock.tick(30)
        screen.fill((0,20,0))
        
        group.update()
        
        group.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
if __name__ == "__main__":
    main()