import  os, sys, pygame, random
import eventhandle, displaylib
from pygame.locals import *

def fall(char,mount,chance):
    d = None
    for x in mount.diff:
        d = x.split('(',')')
        if (char.position <= d[1]):
            break
    fChance = (mount.difficulty + (d[0]/5)) / 2
    if(chance > (fChance/2) * 100):
        return random.randint(1,mount.routelen)
    else: return 0

class Mountain:
    def __init__(self, name, height, difficultyoverall, routelength, difficulties):
        self.name = name
        self.height = height
        self.difficulty = difficultyoverall
        self.routeLength = routelength
        self.diff = difficulties
        self.images = []
    def on_init(self):
        try:
            path  = getpath("../Assets",("mountain" + name.rstrip(' ') + ".txt"))
            with open(path, "r") as f:
                for line in f:
                    path = getpath("../Assets", line)
                    nwIm = image(path)
                    self.images.append(nwIm)
        except:
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
        try:
            path = displaylib.getpath("../Assets",self.fileName)
            with open(os.path.join(path), "r") as f:
                array = []
                for line in f:
                    array.append(line.rstrip('\n'))
        except:
            print( "Could not load the character" )
        self.name = array[0]
        self.mountsClimbed = array[1]
        self.totalmetersclimbed = array[2]
        if (array != None):
            for i in array:
                path = displaylib.getpath("../Assets", i)
                nImage = displaylib.image(path)
                self.images.append(nImage)
    
    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = pos

    
class level:
    def __init__(self, name):
        self.name = name
        self.mounts = []
        self.newchar = climber("climber.txt")
        self.newchar.on_init()
    
    def on_init(self):
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
            height = info[1].rstrip('\n')
            difficulty = info[2].rstrip('\n')
            routelen = info[3].rstrip('\n')
            diffs = info[4].rstrip('\n')
            #diffs = [ x[0] for x in info[4]]
            mount = Mountain(name, height, difficulty, routelen, diffs)
            self.mounts.append(mount)
    
    def success(self, mount):
        win_surf = None
        path = displaylib.getpath("../Assets", "success.png")
        winim = displaylib.image(path)
        mounttext = displaylib.font(24, mount.name, (255,255,255), True)
        routetext = displaylib.font(20, "You climbed: " + mount.routelen + " m",(255,255,255), False)
        win_surf.blits(blit_sequence = (winim._image_surf,(0,0),(mounttext.text_surf, mounttext.f.size),(routetext.text_surf, routetext.f.size)))
        pygame.display.flip()

    def death(self):
        death_surf = None
        deathtext = displaylib.font(36, "You have died", (255,255,255), False)
        death_surf.blit(deathtext.text_surf, deathtext.f.size)
        pygame.display.flip()

    def run_level(self, select):
        levelMount = self.mounts[select]
        self.newchar.setPosition(0)
        ev = eventhandle.CEvent()
        while(True):

            if(self.newchar.position == levelMount.routeLength):
                self.success(levelMount)
                break
            else:
                for event in pygame.event.get():
                   i = ev.on_event(event, self.newchar)
                   
                   if(i != None): 
                       f = fall(self.newchar, levelMount, i)
                       if(f > levelMount.getRouteLength()): self.death()
                       else: self.newchar.setPosition(self.newchar.position - f)
