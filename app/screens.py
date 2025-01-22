from app import screen, clock, current_screen
from app.objects import Button
from config import Config

import pygame

import sys


class Welcome:

    def __init__(self):
        global screen
        screen = pygame.display.set_mode((800, 600))

        self.bg = pygame.image.load('app/assets/welcomeBack.png')
        
        def start():
            global current_screen
            current_screen = Main()
            current_screen.run()
        start_button = pygame.image.load('app/assets/startBtn.png')
        self.start_button = Button(240, 230, start_button.get_width(), start_button.get_height(), start_button, start)
        
        def open_levels():
            global current_screen
            current_screen = Levels()
            current_screen.run()
        levels_button = pygame.image.load('app/assets/levelsBtn.png')
        self.levels_button = Button(310, 393, levels_button.get_width(), levels_button.get_height(), levels_button, open_levels)
        
        def open_settings():
            global current_screen
            current_screen = Settings()
            current_screen.run()
        settings_button = pygame.image.load('app/assets/settingsBtn.png')
        self.settings_button = Button(310, 452, settings_button.get_width(), settings_button.get_height(), settings_button, open_settings)

        self.buttons = [self.start_button, self.levels_button, self.settings_button]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(self.bg, (0, 0))
            
            for e in self.buttons:
                screen.blit(e.surface, (e.x, e.y))
                e.process()

            pygame.display.update()
            clock.tick(1000 / Config.FPS)


class Main:

    def __init__(self):
        global screen
        screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(1000 / Config.FPS)


class Levels:

    def __init__(self):
        global screen
        screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(1000 / Config.FPS)


class Settings:

    def __init__(self):
        global screen
        screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(1000 / Config.FPS)
