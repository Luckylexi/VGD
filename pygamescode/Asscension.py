import  os, sys, pygame, random, ctypes
import eventhandle, AsscensionLib, displaylib
from pygame.locals import *

class Game:
    def __init__(self):
        self._running = True
        self.newImage = None
        self.ev = eventhandle.CEvent()
        self._display_surf = None

    def on_init(self):  
        pygame.init()
        self._display_surf = pygame.display.set_mode((1280,800), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        path = displaylib.getpath(None,'ascensionopenscreen.png')
        self.newImage = displaylib.image(path)
        self.newImage._image_surf = pygame.transform.scale(self.newImage._image_surf, ((1280,800)))
        
        self.beginner = AsscensionLib.level("beginning")

    def render(self):
        self._display_surf.blit(self.newImage._image_surf, (0,0))
        pygame.display.flip()        

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        self.beginner.on_init()

        while( self._running ):
            self.render()
            self.beginner.run_level(0)
            
        self.on_cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.on_execute()

