import pygame, sys, random, time, PIL
from pygame.locals import *
from PIL import Image

pygame.init()
fpsClock = pygame.time.Clock()

res = 640, 480

greyColor = pygame.Color(127, 127, 127)
orangeColor = pygame.Color(255, 127, 0)
purpleColor = pygame.Color(127, 0, 127)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
windowObj = pygame.display.set_mode(res)
pygame.display.set_caption("rPepG")

fontObj = pygame.font.Font('freesansbold.ttf', 16)

tileSize = 32
im = Image.open("tileMap.bmp")
bitMap = im.load()

while True:
    windowObj.fill(greyColor)
    fpsDisplayObj = fontObj.render("%i" % (fpsClock.get_fps()), False, purpleColor)
    
    for x in range(0, res[0]/tileSize):
        for y in range(0, res[1]/tileSize):
            if bitMap[x, y] == 113:
                pygame.draw.rect(windowObj, whiteColor, (x*tileSize, y*tileSize, tileSize, tileSize), 0)
            elif bitMap[x, y] == 0:
                pygame.draw.rect(windowObj, blackColor, (x*tileSize, y*tileSize, tileSize, tileSize), 0)
            #Use a indexing to assign bitMap values to display certain colors/tiles rather than a shit tonne
            #of if statements.
    windowObj.blit(fpsDisplayObj,(0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(60)