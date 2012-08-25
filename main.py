import pygame, sys, random, time, math
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

class camera:
    def __init__(self, xPos, yPos):
        self.xCoord = xPos
        self.yCoord = yPos
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize
    def updatePos(self, xPos, yPos):
        self.xCoord = xPos
        self.yCoord = yPos
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize

for x in range(0, 256):
    column = x % (len(tileArray)/tileSize)
    row = x / (len(tileArray)/tileSize)
    tileSurfaceArray.append(pygame.surfarray.make_surface(tileArray[column * tileSize:column * tileSize + tileSize, row * tileSize: row * tileSize + tileSize]))

print "tileSurfaceArray length:", len(tileSurfaceArray)

camera = camera(0, 0)

#There is an issue with the tiles shifting incorrectly. FIX THIS NOW!

while True:
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    camXDisplayObj = fontObj.render("%r" % (camera.xCoord), False, whiteColor)
    camYDisplayObj = fontObj.render("%r" % (camera.yCoord), False, whiteColor)
    camTileXDisplayObj = fontObj.render("%r" % (camera.xTile), False, whiteColor)
    camTileYDisplayObj = fontObj.render("%r" % (camera.yTile), False, whiteColor)
    
    for x in range(-camera.offsetX, res[0], tileSize):
        for y in range(-camera.offsetY, res[1], tileSize):
            windowObj.blit(tileSurfaceArray[mapArray[((x + camera.offsetX) / tileSize) + camera.xTile][((y + camera.offsetY) / tileSize) + camera.yTile]], (x, y))

    windowObj.blit(fpsDisplayObj, (0, 0))
    windowObj.blit(camXDisplayObj, (0, 16))
    windowObj.blit(camYDisplayObj, (32, 16))
    windowObj.blit(camTileXDisplayObj, (0, 32))
    windowObj.blit(camTileYDisplayObj, (32, 32))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                camera.updatePos(camera.xCoord, camera.yCoord + 8)
            if event.key == K_UP:
                camera.updatePos(camera.xCoord, camera.yCoord - 8)
            if event.key == K_LEFT:
                camera.updatePos(camera.xCoord - 8, camera.yCoord)
            if event.key == K_RIGHT:
                camera.updatePos(camera.xCoord + 8, camera.yCoord)
            
    pygame.display.update()
    fpsClock.tick(60)
