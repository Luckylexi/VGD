import pygame
<<<<<<< HEAD
import  os, sys, random
import AscensionLib, displaylib, eventhandle

=======
import os
import sys
import random
import AsscensionLib
import displaylib
import eventhandle
>>>>>>> 03c10a1b2184da09db24564a49a0585f6b91b39f


class Game:
    def __init__(self):
        self.onHomeScreen = False
        self._running = True
        self.openingScreen = None
        self.Ascensiontitletext = None
        self._display_surf = None
        self.ev = eventhandle.CEvent()
        self.windowSize = None

    def on_init(self):
        self.onHomeScreen = True
        pygame.init()
        pygame.display.set_caption("Ascension (demo)")
        self._display_surf = pygame.display.set_mode(
            (1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.windowSize = [
            self._display_surf.get_width(), self._display_surf.get_height()]
        self._running = True
        self.openingScreen = displaylib.image("ascensionopenscreen.png")
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
            self.openingScreen._image_surf = pygame.transform.scale(
                self.openingScreen._image_surf, (self.windowSize[0], self.windowSize[1]))
            self._display_surf.blit(self.openingScreen._image_surf, (0, 0))
            self._display_surf.blit(
                self.Ascensiontitletext.text_surf, (20, 20))
            self._display_surf.blit(self.startleveltext.text_surf,
                                    (20, self.Ascensiontitletext.text_surf.get_height()+15))
            pygame.display.flip()
        except:
            print(pygame.error())

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        self.on_render()
        while(self._running):
            # pygame.event.post(pygame.event.Event(2))
            for event in pygame.event.get():
                self.ev.on_event(event, theGame, None, None)
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theGame = Game()
    theGame.on_execute()
