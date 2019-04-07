import os
import sys
import pygame
from pygame.locals import *


def getpath(path, filename):
    if(path != None):
        try:
            os.chdir(path)
            return os.path.join(os.getcwd(), filename)
        except OSError as err:
            print("OS error: {0}".format(err))
    else:
        return os.path.join(os.getcwd(), filename)


class image:
    def __init__(self, fileName):
        self.fileName = fileName
        self._image_surf = None
        try:
            self._image_surf = pygame.image.load(self.fileName).convert_alpha()
            # if(scalew != None and scaleh != None):
            #self._image_surf = pygame.transform.smoothscale(self._image_surf, (scalew,scaleh))
        except:
            print(pygame.get_error())
            print("Could not load image")

    def w(self):
        w = self._image_surf.get_width()
        return w

    def h(self):
        return self._image_surf.get_height()


class animation:
    def __init__(self, g, l, images, timing):
        self.game = g
        self.level = l
        self.sequence = images
        self.time = timing
        self.rect1 = None

    def lastImage(self):
        self.rect1 = pygame.Rect(((self.game.windowSize[0]/2 - self.sequence[len(self.sequence) - 1].w()/2), (self.game.windowSize[1] - 3 * (self.sequence[len(
            self.sequence) - 1].h()/4))), ((self.game.windowSize[0]/2 + self.sequence[len(self.sequence) - 1].w()/2), self.sequence[len(self.sequence) - 1].h()/4))
        self.game._display_surf.blit(self.sequence[len(self.sequence) - 1]._image_surf, ((
            self.game.windowSize[0]/2 - self.sequence[len(self.sequence) - 1].w()/2), 0))

    def renderAnim(self, i):
            self.rect1 = pygame.Rect(((self.game.windowSize[0]/2 - i.w()/2), 0), ((self.game.windowSize[0]/2 + i.w()/2), i.h()))
            try:
                self.game._display_surf.blit(
                    i._image_surf, ((self.game.windowSize[0]/2 - i.w()/2), 0))
            except:
                print("Could not load image " +
                      i.fileName + " " + pygame.get_error())
            pygame.time.delay(int(self.time*1000))


class font:
    def __init__(self, size, textline, color, underline):
        self.file = getpath("../Assets", "FrederickatheGreat-Regular.ttf")
        try:
            self.f = pygame.font.Font(self.file, size)
        except:
            print("Could not load font " + self.file + " " + pygame.get_error())
        self.f.set_underline(underline)
        self.text_surf = self.f.render(textline, True, color)
