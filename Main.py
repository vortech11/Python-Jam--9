import csv, yaml
import pygame
import random
from perlin_noise import PerlinNoise

def rebuild():
    global terrain, xpix, ypix
    noise = PerlinNoise(octaves=2, seed=random.randint(0, 1000))
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    converted_matrix = [[1 if num < -.10 
                         else 2 if num > -.10 and num < .25
                         else 3 if num > .25
                         else 0 for num in sublist] for sublist in pic]
    matrix = [[0 for _ in range(xpix)] for _ in range(ypix)]
    with open("Terrain.csv", 'w', newline='') as File:
        csv.writer(File).writerows(converted_matrix)
        File.close()
    with open("Visible.csv", 'w', newline='') as File:
        csv.writer(File).writerows(matrix)
        File.close()

def reader():
    global terrain, visible
    with open("Terrain.csv", 'r') as File:
        terrain = list(csv.reader(File))
        File.close()

    with open("Visible.csv", 'r', newline='') as File:
        visible = list(csv.reader(File))
        File.close()


camerax = 0
cameray = 0

terrain = []
visible = []

xpix, ypix = 30, 18

rebuild()
reader()

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
    global terrain, camerax, cameray, event
    keys=pygame.key.get_pressed()
    mousekey=pygame.mouse.get_pressed()
    mousepos=pygame.mouse.get_pos()
    camerax += keys[pygame.K_LEFT]-keys[pygame.K_RIGHT]
    cameray += keys[pygame.K_UP]-keys[pygame.K_DOWN]
    if keys[pygame.K_r]: 
        rebuild()
        reader()
    if event.type == pygame.MOUSEBUTTONDOWN:
        visible[int((mousepos[1]-(mousepos[1]%w.tilesize))/w.tilesize)][int((mousepos[0]-(mousepos[0]%w.tilesize))/w.tilesize)] = 1
        

class World:
    def __init__(self):
        self.tilesize=25
    
    def show(self):
        global terrain, visible, camerax, cameray, xpix, ypix
        color = (0, 0, 0)
        screen.fill((0, 0, 0))
        for x in range(ypix):
            for z in range(xpix):
                self.drawrect=pygame.Rect(0 + self.tilesize*z + camerax, 0 + self.tilesize*x + cameray, self.tilesize, self.tilesize)
                if int(visible[x][z]) == 0:
                    color = (232, 232, 232)
                else:
                    if int(terrain[x][z]) == 1: color = (36, 50, 255)
                    elif int(terrain[x][z]) == 2: color = (11, 158, 0)
                    elif int(terrain[x][z]) == 3: color = (140, 140, 140)
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