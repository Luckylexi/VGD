import  os, sys, pygame, random
import AsscensionLib, displaylib, eventhandle
from pygame.locals import *

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.newImage = None
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((1366,768), pygame.HWSURFACE)
        self._running = True
        self.newImage = displaylib.image("ascensionopenscreen.png")
        self.newImage._image_surf = pygame.transform.scale(self.newImage._image_surf, (1360,760))
        beginner = AsscensionLib.level("beginning")
        beginner.on_init()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.blit(self.newImage._image_surf,(0,0))
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

