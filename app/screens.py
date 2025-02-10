from app import screen, clock, current_screen
from app.objects import Button, Platform, Ball, Block
from config import Config

import pygame
import json
import sys
import random


class Welcome:

    def __init__(self):
        global screen
        screen = pygame.display.set_mode((800, 600))

        self.bg = pygame.image.load('app/assets/welcomeBack.png')

        def start():
            global current_screen
            with open('app/settings.json', 'r') as file:
                level_id = json.load(file)['current_level']
            current_screen = Main(level_id)
            current_screen.run()

        start_button = pygame.image.load('app/assets/startBtn.png')
        self.start_button = Button(240, 230, start_button.get_width(), start_button.get_height(), start_button, start)

        def open_levels():
            global current_screen
            current_screen = Levels()
            current_screen.run()

        levels_button = pygame.image.load('app/assets/levelsBtn.png')
        self.levels_button = Button(310, 393, levels_button.get_width(), levels_button.get_height(), levels_button,
                                    open_levels)

        def open_settings():
            global current_screen
            current_screen = Settings()
            current_screen.run()

        settings_button = pygame.image.load('app/assets/settingsBtn.png')
        self.settings_button = Button(310, 452, settings_button.get_width(), settings_button.get_height(),
                                      settings_button, open_settings)

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

    def __init__(self, level_id):
        global screen
        screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))

        self.level_id = level_id

        # Загрузка игровых ресурсов
        self.bg = pygame.Surface((Config.SCREEN_W, Config.SCREEN_H))
        self.bg.fill((50, 50, 50))  # Тёмно-серый фон

        # Создание игровых объектов
        self.platform = Platform(Config.SCREEN_W // 2, Config.SCREEN_H - 50)
        self.ball = Ball(Config.SCREEN_W // 2, Config.SCREEN_H - 70)
        self.blocks = []

        # Создание начального расположения блоков
        self.create_blocks()

        # Состояние игры
        self.game_over = False
        self.score = 0
        self.lives = 3

    def create_blocks(self):
        # Чтение файла уровня
        with open(f'app/levels/{self.level_id}.txt', 'r') as file:
            level_data = file.readlines()

        # Создание сетки блоков
        for i, row in enumerate(level_data):
            for j, e in enumerate(row):
                x = j * (Config.BLOCK_WIDTH + 2)
                y = i * (Config.BLOCK_HEIGHT + 2) + 60
                if e == '*':
                    self.blocks.append(Block(x, y))
                elif e == '-':
                    self.blocks.append(Block(x, y, unbreakable=True))

    def run(self):
        global current_screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.game_over:
                # Обновление игровых объектов
                self.platform.update()
                self.ball.update()

                # Проверка столкновений
                self.ball.check_collision(self.platform)

                for block in self.blocks[:]:
                    if self.ball.check_collision(block):
                        if not block.unbreakable:
                            self.blocks.remove(block)
                            self.score += 10

                # Проверка условий победы/поражения
                if len(self.blocks) == 0:
                    self.game_over = True
                    # Переход на следующий уровень
                    self.level_id += 1
                    with open('app/settings.json', 'r') as file:
                        old_data = json.load(file)
                    old_data['current_level'] = self.level_id
                    with open('app/settings.json', 'w') as file:
                        json.dump(old_data, file)
                    try:
                        with open(f'app/levels/{self.level_id}.txt', 'r') as f:
                            # Если файл существует, начинаем новый уровень
                            self.__init__(self.level_id)
                            return
                    except FileNotFoundError:
                        # Если следующего уровня нет, возвращаемся в меню
                        current_screen = Welcome()
                        current_screen.run()

                if self.ball.rect.bottom > Config.SCREEN_H:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                        current_screen = Welcome()
                        current_screen.run()
                    else:
                        self.ball.reset()

            # Отрисовка всех элементов
            screen.blit(self.bg, (0, 0))
            self.platform.draw(screen)
            self.ball.draw(screen)

            for block in self.blocks:
                block.draw(screen)

            # Отображение очков и жизней
            # Отображение очков
            score_text = pygame.font.Font(None, 36).render(f"Очки: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Отображение жизней
            lives_text = pygame.font.Font(None, 36).render(f"Жизни: {self.lives}", True, (255, 255, 255))
            screen.blit(lives_text, (Config.SCREEN_W - 120, 10))

            pygame.display.update()
            clock.tick(Config.FPS)


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
