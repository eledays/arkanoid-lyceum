import pygame
from config import Config
import sys

pygame.init()
pygame.display.set_caption(Config.SCREEN_DESC)

screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))
clock = pygame.time.Clock()

from app.screens import Welcome
current_screen = Welcome()
current_screen.run()

from app import screens