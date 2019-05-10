import os
import sys
import pygame
import random
import eventhandle
import displaylib
import Ascension
from pygame.locals import *


def fall(char, mount, chance):
    dif = mount.diff.split(',')
    stepDiff = None
    fChance = None
    e = []
    for x in dif:
        x = x.strip()
        d = x.split('(')
        d[1] = d[1].strip(')')
        for i in d:
            e.append(int(i))
            mount.stepdiff.append(int(i))
    i = 1
    sum = 0
    while(True):
        sum += e[i]
        if(char.position <= sum):
            stepDiff = e[i-1]/5
            fChance = (float(mount.difficulty) + stepDiff) / 2
            break
        else:
            fChance = 0
        try:
            i += 2
            e[i]
        except:
            break
    if(chance <= ((fChance*100)/2)):
        if(stepDiff*5 == 1):
            return 0
        elif(stepDiff*5 == 2):
            return (random.randint(0, 3))
        elif(stepDiff*5 == 3):
            return (random.randint(0, 9))
        elif(stepDiff*5 == 4):
            return (random.randint(0, 27))
        elif(stepDiff*5 == 5):
            return (random.randint(0, 33))
        else:
            return 0
    else:
        return 0


class Mountain:
    def __init__(self, name, height, difficultyoverall, routelength, difficulties):
        self.name = name
        self.height = height
        self.difficulty = difficultyoverall
        self.routeLength = routelength
        self.diff = difficulties
        self.stepdiff = []
        self.mountImages = []
        self.pathImages = []
        self.other = []

    def on_init(self, Game):
        try:
            fName = self.name.replace(" ", "")
            path = displaylib.getpath("../Assets", (fName + ".txt"))
            with open(path, "r") as self.fallLength:
                for line in self.fallLength:
                    path = displaylib.getpath("../Assets", line)

                    nwIm = displaylib.image(path,0)
                    #nwIm._image_surf = pygame.transform.smoothscale(nwIm._image_surf, ((1366/2),768))
                    w = (Game.windowSize[1]/nwIm.h()) * nwIm.w()
                    nwIm._image_surf = pygame.transform.smoothscale(
                        nwIm._image_surf, (int(w), Game.windowSize[1]))
                    if("path" in path):
                        self.pathImages.append(nwIm)
                    elif(self.name.replace(" ","") in path):
                        self.mountImages.append(nwIm)
                    else:
                        self.other.append(nwIm)
        except:
            print(pygame.get_error())
            print("Could not load the mountain images")

    def getHeight(self):
        return self.height

    def getRouteLength(self):
        return self.routeLength

    def researchIncrement(self):
        return 1 * self.difficulty


class climber:
    def __init__(self, file, game):
        self.game = game
        self.fileName = file
        self.name = None
        self.images = []
        self.position = None
        self.mountsClimbed = 0
        self.totalmetersclimbed = 0
        self.health = 100

    def on_init(self):
        array = []
        try:
            path = displaylib.getpath("../Assets", self.fileName)
            with open(os.path.join(path), "r") as self.fallLength:

                for line in self.fallLength:
                    array.append(line.rstrip('\n'))
        except:
            print("Could not load the character")
        self.name = array[0]
        self.mountsClimbed = int(array[1])
        self.totalmetersclimbed = float(array[2])
        if (array != None):
            for i in array:
                path = displaylib.getpath("../Assets", i)
                nImage = displaylib.image(path,0)
                if (nImage._image_surf != None):
                    w = (self.game.windowSize[1]/nImage.h()) * nImage.w()
                    nImage._image_surf = pygame.transform.smoothscale(
                        nImage._image_surf, (int(w), self.game.windowSize[1]))
                    self.images.append(nImage)

    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = float(pos)

    def getHealth(self):
        return self.health

    def setHealth(self, health):
        self.health = health


class smallScreen:
    def __init__(self, mount):
        self.mountain = mount
        self.imageMap = None

    def on_init(self):
        self.imageMap = self.mountain.images[0]

class Progress:
    def __init__(self, mount, climber):
        self.mountain = mount
        self.cpos = 0
        self.Cprogress = 0
        self.mountmax = 0
        self.climber = climber

    def on_init(self):
        #self.cpos = self.climber.getPosition()
        #self.mountmax = self.mountain.getRouteLength()
        self.Cprogress = 0
        print("Progress max mountain length = " +str(self.mountmax))
        print("Progress player position = " + str(self.cpos))
        #self.Cprogress = self.cpos / mountmax    #may not update tho

    def calcProg(self, climber, mount):
        try:
            self.cpos = climber.getPosition()
            self.mountmax = mount.getRouteLength()
            self.Cprogress = self.cpos / self.mountmax *100
            print(self.Cprogress)
        except:
            print("Could not Calc progress")

    def calcRestProg(self, climber):
        self.climberHealth = self.climber.getHealth() + 5
        return self.climberHealth

    def getProgress(self):
        return self.Cprogress

class level:
    def __init__(self, name, game):
        self.clock = pygame.time.Clock()
        self.name = name
        self.mounts = []
        self.levelMount = None
        self.newchar = climber("climber.txt", game)
        self.newchar.on_init()
        self.dead = False
        self.win = False
        self.game = None
        self.resear = []
        self.fallLength = None
        self.play = False
        self.progress = None
        self.game = game
        self.resear = []
        self.fallLength = None
        self.play = False
        self.walksequence = []
        self.walksounds = []
        
    def on_init(self):
        try:
            levelList = []
            path = displaylib.getpath("../assets", "mountains.txt")
            with open(path, "r") as self.fallLength:
                for line in self.fallLength:
                    levelList.append(line.rstrip('\n'))
        except:
            print("Could not load the level")
        for i in levelList:
            info = (i.split(";"))
            name = info[0]
            height = float(info[1].rstrip('\n'))
            difficulty = float(info[2].rstrip('\n'))
            routelen = float(info[3].rstrip('\n'))
            diffs = info[4].rstrip('\n')
            #diffs = [ x[0] for x in info[4]]
            mount = Mountain(name, height, difficulty, routelen, diffs)
            mount.on_init(self.game)
            self.mounts.append(mount)
            self.resear.append(0)
        try:
            self.walksequence.append(displaylib.animation(self.game, self, [self.newchar.images[0], self.newchar.images[1], self.newchar.images[2], self.newchar.images[3]],0.1))
            self.walksequence.append(displaylib.animation(self.game, self, [self.newchar.images[4], self.newchar.images[5], self.newchar.images[6]],0.1))
        except:
            print("could not load character animation")
            self.walksequence.append(displaylib.image(displaylib.getpath("../assets","leftfoot.png"),0))
            self.walksequence.append(displaylib.image(displaylib.getpath("../assets","rightfoot.png"),0))

        try:
            Ws = []
            path = displaylib.getpath("../assets", "walksounds.txt")
            with open(path, "r") as f:
                for line in f:
                    Ws.append(line.rstrip('\n'))
        except:
            print("could not load walking sounds")

        for i in Ws:
            path = displaylib.getpath("../assets", i)
            newSound = displaylib.sound(path)
            self.walksounds.append(newSound)
    
    def levelSelect(self):
        pass

    def success(self, ev, mount):
        self.clock.tick_busy_loop()
        self.play = False
        self.win = True
        self.newchar.mountsClimbed += 1
        self.newchar.setHealth(100)
        self.newchar.setPosition(0)
        path = displaylib.getpath("../Assets", "success.png")
        winim = displaylib.image(path,0)
        mounttext = displaylib.font(24, mount.name, (255, 255, 255), True)
        routetext = displaylib.font(
            20, "You climbed: " + str(mount.routeLength) + " m", (255, 255, 255), False)
       # timetext = displaylib.font(24, ("Time: {0:.2f} minutes").format(self.clock.get_time()), (255,255,255), False)

        while (True):
            for event in pygame.event.get():
                ev.on_event(event, self.game, self.newchar, self, self.progress)
                self.game._display_surf.fill([0, 0, 0])
                self.game._display_surf.blit(mounttext.text_surf, ((
                    self.game.windowSize[0]/2 - mounttext.text_surf.get_width()), self.game.windowSize[1]/2))
                self.game._display_surf.blit(routetext.text_surf, ((
                    self.game.windowSize[0]/2 - routetext.text_surf.get_width()), self.game.windowSize[1]/2 + 30))
        #        self.game._display_surf.blit(timetext.text_surf, ((
         #           self.game.windowSize[0]/2 - timetext.text_surf.get_width()), self.game.windowSize[1]/2 + 60))
                pygame.display.update()
            if(self.game.onHomeScreen == True):
                break

    def death(self):
        self.play = False
        self.dead = True
        self.newchar.position = 0
        self.game._display_surf.fill([0, 0, 0])
        pygame.display.flip()
        deathtext = displaylib.font(
            36, "You have died", (255, 255, 255), False)
        while (True):
            for event in pygame.event.get():
                self.game._display_surf.fill([0, 0, 0])
                self.game._display_surf.blit(
                    deathtext.text_surf, (self.game.windowSize[0]/2, self.game.windowSize[1]/2))
                pygame.display.flip()
            if(self.game.onHomeScreen == True):
                break

    def rest(self, ev, climber):
        self.res = climber.getHealth()
        self.clock.tick()
        print("Resting Players Health... " + str(self.res))
        print("Resting time passed... " + str(self.clock.get_time()))
        self.clock.tick()
        #self.restMount = self.mounts[mount]



    def research(self):
        pass

    def soundSelect(self):
        i = random.randint(1,len(self.walksounds))
        return self.walksounds[i-1]

    ''' def pathRender(self,move):
        i = random.randint(0,len(self.levelMount.other)-1)
        mountMoveSize = (self.levelMount.stepdiff[1]/self.stepsize) * self.levelMount.mountImages[0].h()
        self.screenpos += mountMoveSize
        if(move):
            self.game._display_surf.blit(self.levelMount.mountImages[0]._image_surf, (int(
                            self.game.windowSize[0]/2 - self.levelMount.mountImages[0].w()/2), self.screenpos))'''

    def levelRender(self):
        self.walkSound = self.soundSelect()
        try:
            falltxt = displaylib.font(20, ("Fall: {0:.2f} m".format(self.fallLength)), [
                255, 255, 255], False)
            healthtxt = displaylib.font(20, ("Health: {0}".format(
                self.newchar.health)), [255, 255, 255], False)
            posText = displaylib.font(
                20, ("Position: {0:.2f} m".format(self.newchar.position)), [255, 255, 255], False)
            progText = displaylib.font(25, ("Progress: {0:.1f} %".format(self.progress.getProgress())), [255,255,255], False)
        except:
            posText = displaylib.font(
                20, "Position: 0 m", [255, 255, 255], False)
            falltxt = displaylib.font(
                20, "Fall: 0 m", [255, 255, 255], False)
            healthtxt = displaylib.font(
                20, "Health: 100", [255, 255, 255], False)
            progText = displaylib.font(25, "Progress: 0.0 %", [255, 255, 255], False)

        self.game._display_surf.fill([0, 0, 0])
        self.game._display_surf.blit(self.levelMount.images[0]._image_surf, (int(
            self.game.windowSize[0]/2 - self.levelMount.images[0].w()/2), 0))

        self.game._display_surf.blit(posText.text_surf, ((
            self.game.windowSize[0] - self.levelMount.images[0].w()), 0))
        self.game._display_surf.blit(falltxt.text_surf, ((
            self.game.windowSize[0] - self.levelMount.images[0].w()), 20))
        self.game._display_surf.blit(healthtxt.text_surf, ((
            self.game.windowSize[0] - self.levelMount.images[0].w()), 40))
        self.game._display_surf.blit(progText.text_surf, ((self.game.windowSize[0] - self.levelMount.images[0].w()), 680))
        if(self.walkswitch == self.prevwalkswitch):
            self.game._display_surf.blit(self.levelMount.images[0]._image_surf, (int(
                        self.game.windowSize[0]/2 - self.levelMount.images[0].w()/2), 0))
            self.walksequence[self.walkswitch].lastImage()
            pygame.display.update()
        else:
            self.walkSound.sound.play()
            for i in self.walksequence[self.walkswitch].sequence:
               
                self.walksequence[self.walkswitch].renderAnim(i)

                pygame.display.update()


    def run_level(self, select):
        self.game.onHomeScreen = False
        self.play = True
        self.levelMount = self.mounts[select]
        self.stepsize = self.levelMount.routeLength/10
        self.newchar.setPosition(0)
        ev = eventhandle.CEvent()
        self.walkswitch = 0
        self.prevwalkswitch = self.walkswitch
        self.progress = Progress(self.levelMount, self.newchar)
        self.progress.on_init()
        self.fallLength = None
        self.clock.tick_busy_loop()
        while self.play:
            while not self.dead:
                if(self.newchar.position >= self.levelMount.routeLength):
                    self.success(ev, self.levelMount)
                    self.rest(ev, self.newchar)
                    break
                else:
                    self.levelRender()
                    self.prevwalkswitch = self.walkswitch
                    for event in pygame.event.get():
                        i = ev.on_event(event, self.game, self.newchar, self, self.progress)
                        if(self.dead == True):
                            break
                        if(i != None):
                            self.fallLength = fall(
                                self.newchar, self.levelMount, i)
                            if((self.newchar.health - self.fallLength) <= 0):
                                self.death()
                                break
                            else:
                                self.newchar.setHealth(
                                    self.newchar.health-self.fallLength)
                                self.fallLength = (
                                    ((self.fallLength/100) * random.randint(self.fallLength, int(self.newchar.position))))
                                self.newchar.setPosition(
                                    self.newchar.position - self.fallLength)
                                break
                    if(self.dead == True):
                        break