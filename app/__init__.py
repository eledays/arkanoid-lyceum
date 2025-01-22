import pygame
from config import Config
import sys


def exit_game():
    sys.exit()


def run_name():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        clock.tick(1000 / Config.FPS)


pygame.init()

screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))
clock = pygame.time.Clock()
run_name()
