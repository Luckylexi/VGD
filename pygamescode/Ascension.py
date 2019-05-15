import pygame
import os
import sys
import random
import AscensionLib
import displaylib
import eventhandle
if os.name == 'nt':
    import win32gui, win32con

class Game:
    def __init__(self):
        self.onHomeScreen = False
        self._running = True
        self.openingScreen = None
        self.Ascensiontitletext = None
        self._display_surf = None
        self.ev = eventhandle.CEvent()
        self.windowSize = None
        self.openingMusic = None

    def on_init(self):
        self.onHomeScreen = True
        pygame.init()
        pygame.mixer.init()
        
        pygame.display.set_caption("Ascension (demo)")
        self._display_surf = pygame.display.set_mode(
            (1280, 720),  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        if os.name == 'nt':
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        self.windowSize = [
            self._display_surf.get_width(), self._display_surf.get_height()]
        self._running = True
        self.openingMusic = displaylib.music(displaylib.getpath("Assets","tobias_weber_-_Between_Worlds_(Instrumental).mp3"))
        openPath = displaylib.getpath("Assets", "ascensionopenscreen.png")
        self.openingScreen = displaylib.image(openPath, 0)
        self.Ascensiontitletext = displaylib.font(
            75, "Ascension", (0, 0, 0), False)
        self.startleveltext = displaylib.font(
            30, "Press Enter to start level", (0, 0, 0), False)

    def set_running(self, run):
        self._running = run

    def on_loop(self):
        pass

    def on_render(self):
        try:
            pygame.display.flip()
            w = (self.windowSize[1]/self.openingScreen.h()*.9) * self.openingScreen.w()
            self.openingScreen.resizeSurf = self.openingScreen.resize(int(w),int(self.windowSize[1]))
            self._display_surf.blit(self.openingScreen.resizeSurf, ((self.windowSize[0]/2 - self.openingScreen.resizeSurf.get_width()/2), self.openingScreen.position))
            self._display_surf.get_width()
            self._display_surf.blit(
                self.Ascensiontitletext.text_surf, ((self._display_surf.get_width()/2 - self.openingScreen.resizeSurf.get_width()/2 + 15), 20))
            self._display_surf.blit(self.startleveltext.text_surf,
                                    ((self.windowSize[0]/2 -  self.openingScreen.resizeSurf.get_width()/2 + 15), self.Ascensiontitletext.text_surf.get_height()+15))
            pygame.display.flip()
        except:
            print(pygame.error())

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        self.on_render()
        self.openingMusic.play()
        while(self._running):
            #pygame.event.post(pygame.event.Event(2))
            for event in pygame.event.get():
                self.ev.on_event(event, self, None)
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theGame = Game()
    theGame.on_execute()
