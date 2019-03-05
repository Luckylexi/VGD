import  os, sys, pygame
from pygame.locals import *


def getpath(path,filename):
    if(path != None):
        os.chdir(path)
        return os.path.join(os.getcwd(), filename)
    else:
        return os.path.join(os.getcwd(), filename)

class image:
    def __init__(self, fileName):
        self.fileName = fileName
        self._image_surf = None
        try:
            self._image_surf = pygame.image.load(fileName).convert_alpha()
        except:
            print("Could not load image")

class font:
    def __init__(self, size, textline, color, underline):
        self.file = getpath("../Assets","FredricktheGreat-Regular.tff")
        self.f = pygame.font.Font(self.file, size)
        self.f.set_underline(underline)
        self.text_surf = self.f.render(textline, True, color)