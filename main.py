import pygame, sys, random, time, math, random, UI
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

#This is used at the bottom of the code in the line with UI.drawInfo
char = pygame.image.load("info/monster_NT.png")

fontObj = pygame.font.Font('freesansbold.ttf', 16)

tiles = pygame.image.load("tiles32.png")
map = pygame.image.load("tileMap.png")
tileArray = pygame.surfarray.pixels3d(tiles)
mapArray = pygame.surfarray.array2d(map)
#See www.pygame.org/docs/ref/surfarray.html for more information.

tileSurfaceArray = []
del map

class Camera:
	#This exists for simplification reasons. It allows us just to simply call a method and update the entire camera.
    def __init__(self, xPos, yPos):
        self.xCoord = xPos
        self.yCoord = yPos
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize
        
    def updatePos(self, xPos, yPos):
	#All methods that exist that update a position will update two seperate values:
	#A value to update the exact x and y and also the tile that the object lies upon.
        self.xCoord = xPos
        self.yCoord = yPos
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize
        
        
class Entity:
	#All entities within the game have a position, a size, and something that determines whether or not it is tangible.
    def __init__(self, xPos, yPos, xSize, ySize, collision):
        self.xCoord = xPos
        self.yCoord = yPos
        self.xSize = xSize
        self.ySize = ySize
        self.xTile = xPos / tileSize
        self.yTile = yPos / tileSize
        self.offsetX = self.xCoord % tileSize
        self.offsetY = self.yCoord % tileSize
        self.coll = collision
        
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
        
	#These two methods exists to test whether or not the entity is alinged with the tile system. It uses the
	#top left as a reference upon whether or not it is in line.
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
	#This class is a little bit more in depth and essentially any object in
	# the game that uses this class would be a npc with health, mana, etc.
	#While all of this information isn't absolutely needed for each npc,
	#The UI will later on need this information. Also, while it is not
	#decided yet, this would allow a player to kill the npcs on will if
	#the designer were to permit it.
    def __init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, collision):
        Entity.__init__(self, xPos, yPos, xSize, ySize, collision)
        self.hp = health
        self.mp = mana
        self.lvl = level
        self.direction = direction
        self.speed = speed
        
    xShift = 0
    yShift = 0
    
	#The following method is my pride and joy. This took so much time that
	#I would honestly rather not think about it. Its purpose is vital to any
	#tile based RPG. Essentially, this code allows a player to shift between
	#tiles with orthagonal direction and remaining clipped to the tiles when
	#the player becomes stationary.
	#!A future note! I would like to implement character speed as a float
	#and that would require a large rewrite of this code. However, I hope that
	#some basic float and integer conversions, it will work out. Maybe not. :/
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
                

class Stats:
	#Python supports multiple inheritance, which is a good thing because
	#that allows us to assign a whole length of fields and methods to certain
	#objects within the game so that we can add this layer of complexity of
	#an RPG only to elements that require it.
    def __init__(self, (strength, dexterity, constitution, intelligence, wisdom, charisma), defense):
        self.str = strength
        self.dex = dexterity
        self.con = constitution
        self.int = intelligence
        self.wis = wisdom
        self.cha = charisma
        self.dfs = defense

#For right now, I have the player object written as a class for
#simplicity's sake. This will allow me to write certain methods
#that only relate to the player.	
class Player(Character, Stats):
    def __init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, coll):
        Character.__init__(self, health, mana, level, speed, direction, xPos, yPos, xSize, ySize, coll)
        
#This little piece of code took quite a lot of time to complete.
#Essentially, it creates an array of all of the tiles that exist
#within the tileArray. Later on, we can call from within this
#new array and take the exact tiles that we need that correspond
#to the specific index on the tileMap.
for x in range(0, 256):
    column = x % (len(tileArray)/tileSize)
    row = x / (len(tileArray)/tileSize)
    tileSurfaceArray.append(pygame.surfarray.make_surface(tileArray[column * tileSize:column * tileSize + tileSize, row * tileSize: row * tileSize + tileSize]))

#For debugging purposes, it just prints how many tiles we have.
print "tileSurfaceArray length:", len(tileSurfaceArray)

#Defining two of the classes here.
camera = Camera(0, 0)
player = Player(20, 20, 10, 6, 0, 256, 256, 32, 32, 1)

while True:
	#We enter the main game loop here. I am defining a few objects that will
	#later be rendered on the screen.
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    posDisplayObj = fontObj.render("%r, %r" % ((player.xCoord), (player.yCoord)), False, whiteColor)
    posTileXDisplayObj = fontObj.render("%r, %r" % ((player.xTile), (player.yTile)), False, whiteColor)

	#We call the position updates of the player and the camera.
    player.shift()
    camera.updatePos(player.xCoord - res[0] / 2 + player.xSize / 2, player.yCoord - res[1] / 2 + player.ySize / 2)
    
	#Here the tiles are rendered on first, allowing other objects to be
	#rendered on top of these tiles.
    for x in range(-camera.offsetX, res[0], tileSize):
        for y in range(-camera.offsetY, res[1], tileSize):
            windowObj.blit(tileSurfaceArray[mapArray[((x + camera.offsetX) / tileSize) + camera.xTile][((y + camera.offsetY) / tileSize) + camera.yTile]], (x, y))
            
	#Here is where we would draw the player, we just draw a rectangle for now.
    pygame.draw.rect(windowObj, whiteColor, (player.xCoord - camera.xCoord, player.yCoord - camera.yCoord, player.xSize, player.ySize))
    
	#Rendering all of the debug info that was created earlier.
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
                
	#Here we render the ui on top of everything else. I do need to change
	#the time of when this is rendered because it can overwrite some other
	#needed information.
    UI.render(25, 25, 10, 10, "Pinksquare Hills", "Pre-alpha")
    UI.drawInfo(char, 78, 100, 24, 28)
    
	#Lastly we call upon the update method of the display object so it will
	#render at the specific time. Also, we specify the frame rate with the
	#tick object on fpsClock.
    pygame.display.update()
    fpsClock.tick(60)