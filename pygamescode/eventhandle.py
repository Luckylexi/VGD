import pygame
import random
import renderingplay
import Ascension

from renderingplay import *
from pygame.locals import *


class CEvent:
    def __init__(self):
        pass

    def on_input_focus(self):
        pass

    def on_input_blur(self):
        pass

    def on_key_down(self, event, game, level, char, prog):
        #keys = [pygame.K_KP_ENTER]
        if event.key == pygame.K_SPACE:
            if(level != None):
                if(level.play == True):
                    if(level.walkswitch == 0):
                        level.walkswitch = 1
                    elif(level.walkswitch == 1):
                        level.walkswitch = 0
                    else:
                        level.walkswitch = 0
                    char.setPosition(
                        (char.getPosition()+(level.levelMount.routeLength/10)))
                    prog.calcProg(char, level.levelMount)
                    return random.randint(0, 100)
        elif event.key == pygame.K_h:
            if(level != None):
                if(level.play == True):
                    if(char.getHealth <= 100): # What if Character is over 100?
                        char.calcRestProg(char) # +5 HP
        
        elif event.key == pygame.K_RETURN:
            if(level != None):
                if(level.play == True):
                    if(level.dead == True):
                        game.onHomescreen = True
                        game.openingMusic.play()
                        game.on_render()
                elif(level.win == True):
                    game.onHomeScreen = True
                    game.openingMusic.play()
                    game.on_render()
            elif(game.onHomeScreen == True):
                print("got here")
                game.openingMusic.stop()
                self.beginner = renderingplay.level("beginning", game)
                self.beginner.on_init()
                game.onHomeScreen = False
                self.beginner.run_level(0)
            else:
                game.onHomeScreen = True
                game.on_render()

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

    def on_resize(self, event, game, level):
        game._display_surf = pygame.display.set_mode(
            event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        game.windowSize = event.dict['size']
        if(level == None):
            game.on_render()

    def on_expose(self):
        pass

    def on_exit(self, game, level):
        if(level != None):
            if(level.play == True):
                level.dead = True
            if(level.win == True):
                game.onHomeScreen = True
        game.set_running(False)

    def on_user(self, event):
        pass

    def on_event(self, event, game, level):
        if event.type == QUIT:
            self.on_exit(game, level)

        elif event.type >= USEREVENT:
            self.on_user(event)

        elif event.type == VIDEOEXPOSE:
            self.on_expose()

        elif event.type == VIDEORESIZE:
            self.on_resize(event, game, level)

        elif event.type == KEYUP:
            self.on_key_up(event)

        elif event.type == KEYDOWN:
            if(level != None):
                i = self.on_key_down(event, game, level, level.newchar, level.progress)
                return i
            else:
                self.on_key_down(event, game, None, None, None)

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
