import pygame, random
import AsscensionLib

from AsscensionLib import *
from pygame.locals import *

class CEvent:
    def __init__(self):
        pass
    def on_input_focus(self):
        pass
    def on_input_blur(self):
        pass
    def on_key_down(self, event, char):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
           char.setPosition((char.getPosition()+10))
           return random.randint(0,101)
    def on_key_up(self, event):
        pass
    def on_mouse_focus(self):
        pass
    def on_mouse_blur(self):
        pass
    def on_minimize(self):
        pass
    def on_restore(self):
        pass
    def on_resize(self,event):
        pass
    def on_expose(self):
        pass
    def on_exit(self):
        pass
    def on_user(self,event):
        pass
    def on_event(self, event, char):
        if event.type == QUIT:
            self.on_exit()
 
        elif event.type >= USEREVENT:
            self.on_user(event)
 
        elif event.type == VIDEOEXPOSE:
            self.on_expose()
 
        elif event.type == VIDEORESIZE:
            self.on_resize(event)
 
        elif event.type == KEYUP:
            self.on_key_up(event)
 
        elif event.type == KEYDOWN:
          i = self.on_key_down(event, char)
          return i
  
        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()