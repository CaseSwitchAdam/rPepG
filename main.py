import pygame, sys, random, time, math
from pygame.locals import *
#Numpy also needs to be installed

pygame.init()
fpsClock = pygame.time.Clock()

tileSize = 32
tileRes = 30, 15
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

class Camera:
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
        
        
class Entity:
    def __init__(self, xPos, yPos, xSize, ySize, tangible):
        self.xCoord = xPos
        self.yCoord = yPos
        self.xSize = xSize
        self.ySize = ySize
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        self.tangible = tangible
        
    def updatePos(self, xPos, yPos):
        self.xCoord = xPos
        self.yCoord = yPos
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        
    def checkXAlign(self):
        if self.xCoord % tileSize:
            return True
        else:
            return False
            
    def checkYAlign(self):
        if self.yCoord % tileSize:
            return True
        else:
            return False
        
        
class Character(Entity):
    def __init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, tangible):
        Entity.__init__(self, xPos, yPos, xSize, ySize, tangible)
        self.hp = health
        self.mp = mana
        self.lvl = level
        self.direction = direction
        self.speed = speed
        
    xShift = 0
    yShift = 0
    
    def shift(self):
        #Alright, so you must make this shift by the speed per frame and also restrict to orthagonal movement.
        #If 0 < tileSize - Coordinate % tileSize <= speed: then snap to next grid.
        #YOU CAN DO THIS!
        
class Player(Character):
    def __init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, tangible):
        Character.__init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, tangible)
        
        
class Monster(Character):
    def __init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, tangible):
        Character.__init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, tangible)
        
    
for x in range(0, 256):
    column = x % (len(tileArray)/tileSize)
    row = x / (len(tileArray)/tileSize)
    tileSurfaceArray.append(pygame.surfarray.make_surface(tileArray[column * tileSize:column * tileSize + tileSize, row * tileSize: row * tileSize + tileSize]))

print "tileSurfaceArray length:", len(tileSurfaceArray)

camera = Camera(0, 0)

monster = Monster(10, 10, 5, 4, 0, 128, 128, 32, 32, 1)
player = Player(20, 20, 10, 4, 0, 256, 256, 32, 32, 1)

while True:
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    camDisplayObj = fontObj.render("%r, %r" % ((player.xCoord), (player.yCoord)), False, whiteColor)
    camTileXDisplayObj = fontObj.render("%r, %r" % ((player.xTile), (player.yTile)), False, whiteColor)
    camTileXDisplayObj = fontObj.render("%r, %r" % ((player.xTile), (player.yTile)), False, whiteColor)

    player.shift()
    camera.updatePos(player.xCoord - res[0] / 2 + player.xSize / 2, player.yCoord - res[1] / 2 + player.ySize / 2)
    
    for x in range(-camera.offsetX, res[0], tileSize):
        for y in range(-camera.offsetY, res[1], tileSize):
            windowObj.blit(tileSurfaceArray[mapArray[((x + camera.offsetX) / tileSize) + camera.xTile][((y + camera.offsetY) / tileSize) + camera.yTile]], (x, y))
            
    pygame.draw.rect(windowObj, whiteColor, (player.xCoord - camera.xCoord, player.yCoord - camera.yCoord, player.xSize, player.ySize))
    
    if monster.xCoord in range(camera.xCoord, camera.xCoord + res[0]) and monster.yCoord in range(camera.yCoord, camera.yCoord + res[1]):
        pygame.draw.rect(windowObj, blackColor, (monster.xCoord - camera.xCoord, monster.yCoord - camera.yCoord, monster.xSize, monster.ySize))
    
    windowObj.blit(fpsDisplayObj, (0, 0))
    windowObj.blit(camDisplayObj, (0, 16))
    windowObj.blit(camTileXDisplayObj, (0, 32))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                player.yShift -= player.speed
            if event.key == K_UP:
                player.yShift += player.speed
            if event.key == K_LEFT:
                player.xShift -= player.speed
            if event.key == K_RIGHT:
                player.xShift += player.speed
        
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                player.yShift += player.speed
            if event.key == K_UP:
                player.yShift -= player.speed
            if event.key == K_LEFT:
                player.xShift += player.speed
            if event.key == K_RIGHT:
                player.xShift -= player.speed
            
    pygame.display.update()
    fpsClock.tick(60)
