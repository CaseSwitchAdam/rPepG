import pygame, sys, random, time
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

tileSizeX = 32
tileSizeY = 32
res = 16, 16

greyColor = pygame.Color(127, 127, 127)
orangeColor = pygame.Color(255, 127, 0)
purpleColor = pygame.Color(127, 0, 127)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
windowObj = pygame.display.set_mode((res[0] * tileSizeX, res[1] * tileSizeY))
pygame.display.set_caption("rPepG")

fontObj = pygame.font.Font('freesansbold.ttf', 16)

tiles = pygame.image.load("tiles32.png")
map = pygame.image.load("tileMap.bmp")
tilesArray = pygame.surfarray.pixels2d(tiles)
#mapArray = pygame.surfarray.array2d(tileMap) #This is the original version that makes a separate array, independent of the original surface
mapArray = pygame.surfarray.pixels2d(map) #This method locks the surface and also cannot use 24-bit data
#However, it is much much faster because the array references to the original Surface. Therefore if you change the array, you change the surface

#Future Note: Create two variables that hold the width/tileSize and the length/tileSize so we can accurately sort through what index to choose.

def getTile(index):
    #Select the tileSize * tileSize part of the tileArray array that corresponds to the index of the mapArray, this is also dependent of the two variables to sort through
    #the tiles Array. Also, it may be beneficial to create an array on start up that will map the index value to x and y coordinates on the mapArray. I'm going to sleep
    surfaceObj = pygame.surfarray.make_surface()
    return surfaceObj

while True:
    windowObj.fill(greyColor)
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    
    for x in range(0, res[0]):
        for y in range(0, res[1]):
            windowObj.blit(getTile(mapArray[x][y]), (x * tileSizeX, y * tileSizeY))

    windowObj.blit(fpsDisplayObj, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(60)