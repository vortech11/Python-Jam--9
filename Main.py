import csv, yaml
import pygame
import random
from perlin_noise import PerlinNoise

def rebuild():
    global world
    noise = PerlinNoise(octaves=2, seed=random.randint(0, 1000))
    xpix, ypix = 30, 18
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    with open("File.csv", 'w', newline='') as File:
        csv.writer(File).writerows(pic)
        File.close()

camerax = 0
cameray = 0

world = []

rebuild()

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

def playerinput():
    global world, camerax, cameray
    keys=pygame.key.get_pressed()
    mousekey=pygame.mouse.get_pressed()
    mousepos=pygame.mouse.get_pos()
    camerax += keys[pygame.K_LEFT]-keys[pygame.K_RIGHT]
    cameray += keys[pygame.K_UP]-keys[pygame.K_DOWN]
    if keys[pygame.K_r]: 
        rebuild()
        with open("File.csv", 'r') as File: 
            world = list(csv.reader(File)) 
            File.close()


class World:
    def __init__(self):
        self.tilesize=25
    
    def show(self):
        global world, camerax, cameray
        screen.fill((0, 0, 0))
        for x in range(len(world)):
            for z in range(len(world[0])):
                self.drawrect=pygame.Rect(0 + self.tilesize*z + camerax, 0 + self.tilesize*x + cameray, self.tilesize, self.tilesize)
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
    
    playerinput()
    w.show()
    
    fps_counter()
    pygame.display.update()

pygame.quit()