import pygame
from pygame.locals import *
import sys
import random

Scr_rect = Rect(0, 0, 500, 500)

class DogSprite(pygame.sprite.Sprite):
    move_height = 100

    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.y = y
        self.vx = vx
        self.vy = vy
        self.up = self.move_height
        self.down = self.up + self.move_height
        self.enabled = True
        self.frame_count = self.move_height* 2 / abs(self.vy)
        self.time = self.frame_count

    def move(self):
            if self.time >= self.frame_count:
                self.time = 0
                self.enabled = True

    def update(self):
        if self.time >= self.frame_count:
            self.enabled = False
            self.rect.top = self.y
            return

        else: 
            if self.time < self.frame_count // 2:
                dy = self.vy
            else:
                dy = -self.vy
            self.time += 1
        
        self.rect.top += dy

    def is_clicked(self, event, pos):
        x,y = event.pos
        print(x,y)
        if self.enabled and self.rect.collidepoint(x,y) and y <= 203:
            self.enabled = False
            return True

        return False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    pygame.init()
    cl = pygame.time.Clock()
    screen = pygame.display.set_mode(Scr_rect.size)
    pygame.display.set_caption("Game")

    font = pygame.font.SysFont(None, 78)
    font2 = pygame.font.SysFont(None, 45)
    font3 = pygame.font.SysFont(None, 30)
    text1 = font.render("Click!", True, (204, 102, 112))
    text2 = font2.render("+1", True, (0, 0, 0))
    click = 0
    score = 0
    n_frames = 0
    TIME_END = 20
    random1 = [random.randint(0, TIME_END*30) for i in range(10)]
    random2 = [random.randint(0, TIME_END*30) for i in range(10)]
    random3 = [random.randint(0, TIME_END*30) for i in range(10)]

    line = pygame.image.load("line.png").convert()
    colorkey = line.get_at((0,0))
    line.set_colorkey(colorkey,RLEACCEL)
    wall = pygame.image.load("wall.png")
    #Spriteを作成
    dog1 = DogSprite("dog.png", 65, 215, 0, -5)
    dog2 = DogSprite("dog.png", 215, 215, 0, -3)
    dog3 = DogSprite("dog.png", 365, 215, 0, -4)
    #Groupを作成
    group = pygame.sprite.RenderUpdates()
    group.add(dog1)
    group.add(dog2)
    group.add(dog3)
 
    while (1):
        screen.fill((102, 204, 194))
        screen.blit(text1, [170, 30])
        rest = TIME_END - (n_frames / 30)
        text4 = font3.render('time: {}'.format(round(rest,1)), True, (0, 0, 0))
        screen.blit(text4,[350,60])

        if n_frames in random1:
            dog1.move()
        
        if n_frames in random2:
            dog2.move()

        if n_frames in random3:
            dog3.move()
        
        if n_frames < 30 * TIME_END:
            group.update()

        group.draw(screen)
        screen.blit(wall, (0, 208))
        screen.blit(line, (50, 173))
        screen.blit(line, (200, 173))
        screen.blit(line, (350, 173))

        for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()
           
            if n_frames < 30 * TIME_END and event.type == MOUSEBUTTONDOWN and event.button == 1:
                if dog1.is_clicked(event, event.pos) or dog2.is_clicked(event, event.pos) or dog3.is_clicked(event, event.pos):
                    click = 9
                    score += 1

        text3 = font3.render('score : {}'.format(score), True, (0, 0, 0))
        screen.blit(text3, [350, 40] )
        
        if click > 0:
            pos = pygame.mouse.get_pos()
            screen.blit(text2, pos)
            click -= 1
        pygame.display.update()

        if n_frames < 30 * TIME_END:
             n_frames += 1

        cl.tick(30)

if __name__ == "__main__":
    main()
