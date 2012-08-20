import pygame, sys, random, time
from pygame.locals import *
#Numpy also needs to be installed

pygame.init()
fpsClock = pygame.time.Clock()

tileSize = 32
tileRes = 16, 16
res = tileRes[0] * tileSize, tileRes[1] * tileSize

greyColor = pygame.Color(127, 127, 127)
orangeColor = pygame.Color(255, 127, 0)
purpleColor = pygame.Color(127, 0, 127)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
windowObj = pygame.display.set_mode(res)
pygame.display.set_caption("rPepG")

fontObj = pygame.font.Font('freesansbold.ttf', 16)

tiles = pygame.image.load("tiles32.png")
map = pygame.image.load("tileMap.png")
tileArray = pygame.surfarray.pixels3d(tiles)
mapArray = pygame.surfarray.array2d(map)
#See www.pygame.org/docs/ref/surfarray.html for more information.

tileSurfaceArray = []
del map

for x in range(0, 256):
    column = x % (len(tileArray)/tileSize)
    row = int(x / (len(tileArray)/tileSize))
    tileSurfaceArray.append(pygame.surfarray.make_surface(tileArray[column * tileSize:column * tileSize + tileSize, row * tileSize: row * tileSize + tileSize]))

print "tileSurfaceArray length:", len(tileSurfaceArray)

while True:
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    
    for x in range(0, res[0], tileSize):
        for y in range(0, res[1], tileSize):
            windowObj.blit(tileSurfaceArray[mapArray[x / tileSize][y / tileSize]], (x, y))

    windowObj.blit(fpsDisplayObj, (0, 0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(60)
