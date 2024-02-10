import csv, yaml
import pygame
import random
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=2, seed=random.randint(0, 1000))
xpix, ypix = 30, 18
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

with open("File.csv", 'w', newline='') as File:
    csv.writer(File).writerows(pic)
    File.close()

with open("File.csv", 'r') as File:
    world = list(csv.reader(File))
    File.close()

with open("config.yaml", "r") as yamlfile:
    settings = yaml.safe_load(yamlfile)
    yamlfile.close()


pygame.init()
W, H=settings['W'], settings['H']
screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Game Thing")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial" , 12 , bold = True)

running = True

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))

class World:
    def __init__(self):
        self.tilesize=25
    
    def show(self):
        global world
        for x in range(len(world)):
            for z in range(len(world[0])):
                self.drawrect=pygame.Rect(0 + self.tilesize*z, 0 + self.tilesize*x, self.tilesize, self.tilesize)
                if world[x][z] < str(-.5): color = (36, 50, 255)
                elif world[x][z] > str(.5): color = (140, 140, 140)
                elif world[x][z] > str(-.5) and world[x][z] < str(.5): color = (11, 158, 0)

                pygame.draw.rect(screen, color, self.drawrect)


w=World()
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    w.show()

    fps_counter()
    pygame.display.update()

pygame.quit()