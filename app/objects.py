from app import screen

import pygame


class Button:

    def __init__(self, x, y, width, height, surface, onclick):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = surface
        self.onclick = onclick

        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.onclick()