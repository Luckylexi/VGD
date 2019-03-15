import  os, sys, pygame, random
import eventhandle, displaylib, Asscension
from pygame.locals import *

def fall(char,mount,chance):
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
    f = 1
    sum = 0
    while(True):
        sum += e[f]
        if(char.position <= sum):
            stepDiff = e[f-1]/5
            fChance = (float(mount.difficulty) + stepDiff) / 2
            break
        try:
            f+= 2
            e[f]
        except:
            break
    if (fChance != None):
        if(chance < ((fChance/2) * 100)):
            if(stepDiff*5 == 1):
                return 0
            if(stepDiff*5 == 2):
                return random.randint(1, int(mount.routeLength/250))
            elif(stepDiff*5 == 3):
                return random.randint(1, int(2 * mount.routeLength/100))
            elif(stepDiff*5 == 4):
                return random.randint(1, int(3 * mount.routeLength/100))
            elif(stepDiff*5 == 5):
                return random.randint(1, int(4 * mount.routeLength))
        else: return 0
    else: return 0

class Mountain:
    def __init__(self, name, height, difficultyoverall, routelength, difficulties):
        self.name = name
        self.height = height
        self.difficulty = difficultyoverall
        self.routeLength = routelength
        self.diff = difficulties
        self.images = []
    def on_init(self, Game):
        try:
            fName = self.name.replace(" ", "")
            path  = displaylib.getpath("../Assets",(fName + ".txt"))
            with open(path, "r") as f:
                for line in f:
                    path = displaylib.getpath("../Assets", line)
                    
                    nwIm = displaylib.image(path)
                    #nwIm._image_surf = pygame.transform.smoothscale(nwIm._image_surf, ((1366/2),768))
                    w = (Game.windowSize[1]/nwIm.h()) * nwIm.w()
                    nwIm._image_surf = pygame.transform.smoothscale(nwIm._image_surf, (int(w), Game.windowSize[1]))
                    
                    self.images.append(nwIm)
        except:
            print(pygame.get_error())
            print( "Could not load the mountain images" )
    def getHeight(self):
        return self.height
    def getRouteLength(self):
        return self.routeLength

class smallScreen:
    def __init__(self, mount):
        self.mountain = mount
        self.imageMap = None
    def on_init(self):
        self.imageMap = self.mountain.images[0]
        
class climber:
    def __init__(self, file):
        self.fileName = file
        self.name = None
        self.images = []
        self.position = None
        self.mountsClimbed = 0
        self.totalmetersclimbed = 0

    def on_init(self):
        array = []
        try:
            path = displaylib.getpath("../Assets",self.fileName)
            with open(os.path.join(path), "r") as f:
                
                for line in f:
                    array.append(line.rstrip('\n'))
        except:
            print( "Could not load the character" )
        self.name = array[0]
        self.mountsClimbed = int(array[1])
        self.totalmetersclimbed = float(array[2])
        if (array != None):
            for i in array:
                path = displaylib.getpath("../Assets", i)
                nImage = displaylib.image(path)
                if (nImage._image_surf != None):
                    self.images.append(nImage)
    
    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = float(pos)

    
class level:
    def __init__(self, name):
        self.name = name
        self.mounts = []
        self.newchar = climber("climber.txt")
        self.newchar.on_init()
        self.dead = False
        self.win = False
        self.game = None

    
    def on_init(self,game):
        self.game = game
        try:
            levelList = []
            path = displaylib.getpath("../assets","mountains.txt")
            with open(path, "r") as f:
                for line in f:
                    levelList.append(line.rstrip('\n'))       
        except:
           print( "Could not load the level" )
        for i in levelList:
            info = (i.split(";"))
            name = info[0]
            height = float(info[1].rstrip('\n'))
            difficulty = float(info[2].rstrip('\n'))
            routelen = float(info[3].rstrip('\n'))
            diffs = info[4].rstrip('\n')
            #diffs = [ x[0] for x in info[4]]
            mount = Mountain(name, height, difficulty, routelen, diffs)
            mount.on_init(game)
            self.mounts.append(mount)
    
    def success(self, mount):
        path = displaylib.getpath("../Assets", "success.png")
        winim = displaylib.image(path)
        mounttext = displaylib.font(24, mount.name, (255,255,255), True)
        routetext = displaylib.font(20, "You climbed: " + str(mount.routeLength) + " m",(255,255,255), False)
        self.game._display_surf.fill([0,0,0])
        self.game._display_surf.blit(mounttext.text_surf,((self.game.windowSize[0]/2 - mounttext.text_surf.get_width()),self.game.windowSize[1]/2))
        self.game._display_surf.blit(routetext.text_surf,((self.game.windowSize[0]/2 - routetext.text_surf.get_width()),self.game.windowSize[1]/2 + 30))
        pygame.display.flip()


    def death(self):
        self.newchar.position = 0
        deathtext = displaylib.font(36, "You have died", (255,255,255), False)
        self.game._display_surf.fill([0,0,0])
        self.game._display_surf.blit(deathtext.text_surf, (self.game.windowSize[0]/2, self.game.windowSize[1]/2))
        pygame.display.flip()
        return True

    def run_level(self, select):
        self.levelMount = self.mounts[select]
        self.newchar.setPosition(0)
        
        ev = eventhandle.CEvent()
        self.walkswitch = 0
        f = None
        while not self.dead:

            self.game._display_surf.fill([0,0,0])
            self.game._display_surf.blit(self.levelMount.images[0]._image_surf,(int(self.game.windowSize[0]/2 - self.levelMount.images[0].w()/2),0))
            posText = displaylib.font(20, ("Position: " + f"{self.newchar.position: .1f}" + " m"), [255,255,255], False)
            self.game._display_surf.blit(posText.text_surf, ((self.game.windowSize[0] - self.levelMount.images[0].w()),0))
            
            self.game._display_surf.blit(self.newchar.images[self.walkswitch]._image_surf, (self.game.windowSize[0]/2 - (self.levelMount.images[0].w()/4), 2*self.game.windowSize[1]/3))
            
            if(self.newchar.position >= self.levelMount.routeLength):
                self.success(self.levelMount)
                self.newchar.mountsClimbed += 1
                pygame.time.wait(3000)
                break
            else:
                for event in pygame.event.get():   
                    i = ev.on_event(event, self.game, self.newchar, self)
                    if(self.dead == True):
                        break
                    if(i != None): 
                       f = fall(self.newchar, self.levelMount, i)
                       if(f > self.newchar.position): 
                           self.dead = self.death()
                       else: self.newchar.setPosition(self.newchar.position - f)
                if(self.dead == True):
                    break
                if(f != None):
                    falltxt = displaylib.font(20, "Fall: " + str(f) + " m", [255,255,255], False)
                else:
                    falltxt = displaylib.font(20, "Fall: 0 m", [255,255,255], False)
            
            self.game._display_surf.blit(falltxt.text_surf, ((self.game.windowSize[0] - self.levelMount.images[0].w()),20))
            pygame.display.flip()
                    
