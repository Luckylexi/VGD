import  os, sys, pygame, random
from pygame.locals import *


class image:
    def __init__(self, fileName):
        self.fileName = fileName

class Mountain:
    def __init__(self, name, height, difficultyoverall, routelength, difficulties):
        self.name = name
        self.height = height
        self.difficulty = difficultyoverall
        self.routeLength = routelength
        self.diff = difficulties
    def on_init (self):
        percent = []
        for x in self.diff:
            percent.append((self.diff[x] * self.difficulty))

        return percent

class level:
    def __init__(self, name):
        self.name = name
        self.mounts = []
        self.images = []
    def on_init(self):
        try:
            cwd  = os.getcwd()
            with open(os.path.join(cwd, "mountains.txt"), "r") as f:
                array = []
                for line in f:
                    array.append(line.rstrip('\n'))
        except:
            "Could not load the level"
        
        for i in array:
            info = (array[i].split(", "))
            mount = Mountain(info[0], info[1], info[2], info[3], info[4])
            self.mounts.append(mount)
            

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.newImage = image('ascensionopenscreen.png')
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((1366,768), pygame.HWSURFACE)
        self._running = True
        cwd = os.getcwd()
        self._image_surf = pygame.image.load(os.path.join(cwd, 'ascensionopenscreen.png')).convert_alpha()
        self._image_surf = pygame.transform.scale(self._image_surf, (1360,760))
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.on_execute()

