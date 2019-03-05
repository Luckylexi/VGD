import  os, sys, pygame, random
import eventhandle, AsscensionLib, displaylib
from pygame.locals import *

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.newImage = None
        self.ev = eventhandle.CEvent()

    def on_init(self):  
        pygame.init()
        self._display_surf = pygame.display.set_mode((1366,768), pygame.HWSURFACE)
        self._running = True
        path = displaylib.getpath(None,'ascensionopenscreen.png')
        self.newImage = displaylib.image(path)
        self.newImage._image_surf = pygame.transform.scale(self.newImage._image_surf, (1360,760))
        self.beginner = AsscensionLib.level("beginning")
        

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        self.beginner.on_init()

        while( self._running ):
            self.beginner.run_level(0)
        self.on_cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.on_execute()

