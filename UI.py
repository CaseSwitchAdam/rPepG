import pygame, sys
from pygame.locals import *
def getJob():
    print "One does not simply 'get a job'"

pygame.init()
fpsClock = pygame.time.Clock()

windowObj = pygame.display.set_mode((640, 480))
pygame.display.set_caption('UI Test: Health gauge')

manabar = pygame.image.load("status/ManaBar.png")
healthbar = pygame.image.load("status/HealthBar.png")
emptybar = pygame.image.load("status/EmptyBar.png")
infobubble = pygame.image.load("info/infobubble.png")
infotab = pygame.image.load("info/info.png")
smallmanabar = pygame.image.load("info/ManaBar.png")
smallhealthbar = pygame.image.load("info/HealthBar.png")
transhealthbar = pygame.image.load("info/HealthBar.png")
transmanabar = pygame.image.load("info/ManaBar.png")
smallemptybar = pygame.image.load("info/EmptyBar.png")
char = pygame.image.load("info/monster_NT.png")
preview = pygame.image.load("status/spartan.png")


red = pygame.Color(172, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 72, 140)
white = pygame.Color(255, 255, 255)
orange = pygame.Color(255, 164, 5)
black = pygame.Color(0, 0, 0)
gray = pygame.Color(128, 128, 128)


mousex, mousey = 0, 0
world = "Overworld"
bauhausFont = pygame.font.Font('fonts/BAUHS93.TTF', 22)
agencyFont = pygame.font.Font('fonts/AGENCYR.TTF', 20)
smAgencyFont = pygame.font.Font('fonts/AGENCYR.TTF', 12)
healthSquareLoc = (8, 8)
healthUI = pygame.image.load("status/UI_Health.png")





def drawBubble(xloc, yloc, name, hpcur, hpmax, mpcur, mpmax, str, lv):
    # The location refers to the tip of the bubble.
    windowObj.blit(infobubble, (xloc, yloc - 146))
#    bauhausFont.render(str, AA, color)
    windowObj.blit(bauhausFont.render("%s - Lv. %d" % (name, lv), True, white), (xloc + 16, yloc - 138))
    windowObj.blit(bauhausFont.render("STR: %d" % str, True, white), (xloc + 16, yloc - 118))
    for x in range(0, hpmax):
        pygame.draw.rect(windowObj, black, (xloc + 184 - x * 8, yloc - 39, 8, 24))
        if hpcur > x:
            pygame.draw.rect(windowObj, red, (xloc + 185 - x * 8, yloc - 38, 6, 22))
        else:
            pygame.draw.rect(windowObj, gray, (xloc + 185 - x * 8, yloc - 38, 6, 22))
    for x in range(0, mpmax):
        pygame.draw.rect(windowObj, black, (xloc + 184 - x * 8, yloc - 63, 8, 24))
        if hpcur > x:
            pygame.draw.rect(windowObj, blue, (xloc + 185 - x * 8, yloc - 62, 6, 22))
        else:
            pygame.draw.rect(windowObj, gray, (xloc + 185 - x * 8, yloc - 62, 6, 22))
def drawInfo(image, health1, health2, mana1, mana2):
    topleft = (540, 430)
    windowObj.blit(char, (topleft[0] + 57, topleft[1] + 5))
    windowObj.blit(infotab, (topleft))
    for x in range(0, 5):
        if x == int(5 * mana1 / mana2):
            mperbar = float(mana2) / 5
            mcurbar = mana1 - (x * mperbar)
            mpercent = mcurbar / mperbar
            transmanabar.set_alpha(mpercent * 255)
            windowObj.blit(smallemptybar, (topleft[0] + 15 - (10 * x), topleft[1]))
            windowObj.blit(transmanabar, (topleft[0] + 15 - (10 * x), topleft[1]))
        elif .2 * x < float(mana1) / mana2:
            windowObj.blit(smallemptybar, (topleft[0] + 15 - (10 * x), topleft[1]))
            windowObj.blit(smallmanabar, (topleft[0] + 15 - (10 * x), topleft[1]))
        else:
            windowObj.blit(smallemptybar, (topleft[0] + 15 - (10 * x), topleft[1]))
    for x in range(0, 5):
        if x == int(5 * health1 / health2):
            perbar = float(health2) / 5
            curbar = health1 - (x * perbar)
            hpercent = curbar / perbar
            transhealthbar.set_alpha(hpercent * 255)
            windowObj.blit(smallemptybar, (topleft[0] - (10 * (x + 1)), topleft[1] + 25))
            windowObj.blit(transhealthbar, (topleft[0] - (10 * (x + 1)), topleft[1] + 25))
        elif .2 * x < float(health1) / health2:
            windowObj.blit(smallemptybar, (topleft[0] - (10 * (x + 1)), topleft[1] + 25))
            windowObj.blit(smallhealthbar, (topleft[0] - (10 * (x + 1)), topleft[1] + 25))
        else:
            windowObj.blit(smallemptybar, (topleft[0] - (10 * (x + 1)), topleft[1] + 25))

def render(health1, health2, mana1, mana2, msg, msg2):
    pygame.draw.rect(windowObj, white, (8, 8, 64, 64))
    windowObj.blit(healthUI, (0,0))
    windowObj.blit(preview, (16, 16))
    windowObj.blit(agencyFont.render(msg, True, white), (80, 8))
    windowObj.blit(smAgencyFont.render(msg2, True, white), (80, 28))
    for x in range(0, int(health2)):
        if health1 > x:
            windowObj.blit(healthbar, (260 + 10 * x, 0))
        else:
            windowObj.blit(emptybar, (260 + 10 * x, 0))
    for x in range(0, int(mana2)):
        if mana1 > x:
            windowObj.blit(manabar, (220 + 10 * x, 40))
        else:
            windowObj.blit(emptybar, (220 + 10 * x, 40))