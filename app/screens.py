from app import screen, clock
from config import Config

import pygame

import sys


class Welcome:

    def __init__(self):
        self.bg = pygame.image.load('app/assets/welcomeBack.png')
        self.start_button = pygame.image.load('app/assets/startBtn.png')
        self.levels_button = pygame.image.load('app/assets/levelsBtn.png')
        self.settings_button = pygame.image.load('app/assets/settingsBtn.png')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(self.bg, (0, 0))
            screen.blit(self.start_button, (240, 230))
            screen.blit(self.levels_button, (310, 393))
            screen.blit(self.settings_button, (310, 452))

            pygame.display.update()
            clock.tick(1000 / Config.FPS)