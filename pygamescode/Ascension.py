import  os, sys, pygame, random
import AsscensionLib, displaylib, eventhandle
from pygame.locals import *

class Game:
    def __init__(self):
        self._running = True
        self.newImage = None
        self._display_surf = None
        self.ev = eventhandle.CEvent()
        self.windowSize = None
 
    def on_init(self):
        pygame.init() 
        pygame.display.set_caption("Ascension (demo)")
        self._display_surf = pygame.display.set_mode((1280,720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE )
        self.windowSize = [self._display_surf.get_width(),self._display_surf.get_height()]
        self._running = True
        self.newImage = displaylib.image("ascensionopenscreen.png")
        
        self.startleveltext = displaylib.font(30, "Press Enter to start level", (0,0,0), False)

    def set_running(self, run):
        self._running = run

    def on_loop(self):
        pass
    def on_render(self):
        try:
            pygame.display.init()
            self.newImage._image_surf = pygame.transform.scale(self.newImage._image_surf, (self.windowSize[0],self.windowSize[1]))
            self._display_surf.blit(self.newImage._image_surf,(0,0))
            self._display_surf.blit(self.startleveltext.text_surf, (self.windowSize[0]/2,self.windowSize[1]/2))
            pygame.display.flip()
        except: 
            print(pygame.error())
        
 
    def on_cleanup(self): 
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running  = False
        self.on_render()
        while( self._running ):
            #pygame.event.post(pygame.event.Event(2))
            for event in pygame.event.get():
                self.ev.on_event(event, theGame, None, None)
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.on_execute()

