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


class font:
    def __init__(self, size, textline, color, underline):
        self.file = getpath("../Assets", "FrederickatheGreat-Regular.ttf")
        try:
            self.f = pygame.font.Font(self.file, size)
        except:
            print("Could not load font " + self.file + " " + pygame.get_error())
        self.f.set_underline(underline)
        self.text_surf = self.f.render(textline, True, color)
