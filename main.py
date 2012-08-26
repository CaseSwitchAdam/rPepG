import pygame, sys, random, time, math
from pygame.locals import *
#Numpy also needs to be installed

pygame.init()
fpsClock = pygame.time.Clock()

tileSize = 32
tileRes = 20, 15
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
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize
        self.tangible = tangible
        
    def updateXPos(self, xPos):
        self.xCoord = xPos
        self.xTile = xPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize
        
    def updateYPos(self, yPos):
        self.yCoord = yPos
        self.yTile = yPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize        
        
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
            
    xVelocity = 0
    yVelocity = 0
        
        
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
        if self.xShift == 0 and self.xVelocity != 0 and self.yShift == 0: #Initial X Movement
            self.xShift = math.copysign(1, self.xVelocity)
            self.updateXPos(self.xVelocity + self.xCoord)
        elif self.xShift == -1: #Left Snap
            if 0 <= self.offsetX <= self.speed:
                self.updateXPos(self.xCoord - self.offsetX)
                self.xShift = 0
            else:
                self.updateXPos(self.xCoord - self.speed)
        elif self.xShift == 1: #Right Snap
            if 0 < (tileSize - self.offsetX) <= self.speed:
                self.updateXPos(self.xCoord + (tileSize - self.offsetX))
                self.xShift = 0
            else:
                self.updateXPos(self.xCoord + self.speed)
        elif self.yShift == 0 and self.yVelocity != 0 and self.xShift == 0: #Initial Y Movement
            self.yShift = math.copysign(1, self.yVelocity)
            self.updateYPos(self.yVelocity + self.yCoord)
        elif self.yShift == -1: #Up Snap
            if 0 <= self.offsetY <= self.speed:
                self.updateYPos(self.yCoord - self.offsetY)
                self.yShift = 0
            else:
                self.updateYPos(self.yCoord - self.speed)
        elif self.yShift == 1: #Down Snap
            if 0 < (tileSize - self.offsetY) <= self.speed:
                self.updateYPos(self.yCoord + (tileSize - self.offsetY))
                self.yShift = 0
            else:
                self.updateYPos(self.yCoord + self.speed)
        
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
player = Player(20, 20, 10, 3, 0, 256, 256, 32, 32, 1)

while True:
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    posDisplayObj = fontObj.render("%r, %r" % ((player.xCoord), (player.yCoord)), False, whiteColor)
    posTileXDisplayObj = fontObj.render("%r, %r" % ((player.xTile), (player.yTile)), False, whiteColor)

    player.shift()
    camera.updatePos(player.xCoord - res[0] / 2 + player.xSize / 2, player.yCoord - res[1] / 2 + player.ySize / 2)
    
    for x in range(-camera.offsetX, res[0], tileSize):
        for y in range(-camera.offsetY, res[1], tileSize):
            windowObj.blit(tileSurfaceArray[mapArray[((x + camera.offsetX) / tileSize) + camera.xTile][((y + camera.offsetY) / tileSize) + camera.yTile]], (x, y))
            
    pygame.draw.rect(windowObj, whiteColor, (player.xCoord - camera.xCoord, player.yCoord - camera.yCoord, player.xSize, player.ySize))
    
    if monster.xCoord in range(camera.xCoord - monster.xSize, camera.xCoord + res[0]) and monster.yCoord in range(camera.yCoord - monster.ySize, camera.yCoord + res[1]):
        pygame.draw.rect(windowObj, blackColor, (monster.xCoord - camera.xCoord, monster.yCoord - camera.yCoord, monster.xSize, monster.ySize))
    
    windowObj.blit(fpsDisplayObj, (0, 0))
    windowObj.blit(posDisplayObj, (0, 16))
    windowObj.blit(posTileXDisplayObj, (0, 32))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                player.yVelocity -= player.speed
            elif event.key == K_UP:
                player.yVelocity += player.speed
            elif event.key == K_LEFT:
                player.xVelocity += player.speed
            elif event.key == K_RIGHT:
                player.xVelocity -= player.speed
        
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                player.yVelocity += player.speed
            elif event.key == K_UP:
                player.yVelocity -= player.speed
            elif event.key == K_LEFT:
                player.xVelocity -= player.speed
            elif event.key == K_RIGHT:
                player.xVelocity += player.speed
            
    pygame.display.update()
    fpsClock.tick(60)
