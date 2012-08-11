import pygame, sys, random, time
from pygame.locals import *
#Numpy also needs to be installed

pygame.init()
fpsClock = pygame.time.Clock()

tileSize = 32
res = 16, 16

greyColor = pygame.Color(127, 127, 127)
orangeColor = pygame.Color(255, 127, 0)
purpleColor = pygame.Color(127, 0, 127)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
windowObj = pygame.display.set_mode((res[0] * tileSize, res[1] * tileSize))
pygame.display.set_caption("rPepG")

fontObj = pygame.font.Font('freesansbold.ttf', 16)

tiles = pygame.image.load("tiles32.png")
map = pygame.image.load("tileMap.bmp")
tileArray = pygame.surfarray.pixels2d(tiles)
#mapArray = pygame.surfarray.array2d(tileMap) #This is the original version that makes a separate array, independent of the original surface
mapArray = pygame.surfarray.pixels2d(map) #This method locks the surface and also cannot use 24-bit data
#However, it is much much faster because the array references to the original Surface. Therefore if you change the array, you change the surface

tileArrayWidth = len(tileArray)/tileSize
tileSurfaceArray = []

for x in range(0, 256):
    column = x % tileArrayWidth
    row = int(x / tileArrayWidth)
    print column * tileSize,column * tileSize + tileSize, row * tileSize, row * tileSize + tileSize
    tileSurfaceArray.append(pygame.surfarray.make_surface(tileArray[column * tileSize:column * tileSize + tileSize, row * tileSize: row * tileSize + tileSize]))
    
del tileArray
print len(tileSurfaceArray)

while True:
    windowObj.fill(greyColor)
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    
    for x in range(0, res[0]):
        for y in range(0, res[1]):
            windowObj.blit(tileSurfaceArray[mapArray[x][y]], (x * tileSize, y * tileSize))

    windowObj.blit(fpsDisplayObj, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(60)