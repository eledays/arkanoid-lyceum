from app import screen, clock, current_screen
from app.objects import Button, Platform, Ball, Block
from config import Config

import pygame
import json
import sys
import os


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
        print(level_id)
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

        with open('app/settings.json', 'r') as file:
            settings = json.load(file)

        # Создание сетки блоков
        for i, row in enumerate(level_data):
            for j, e in enumerate(row):
                x = j * (Config.BLOCK_WIDTH + 2)
                y = i * (Config.BLOCK_HEIGHT + 2) + 60
                if e == '*':
                    self.blocks.append(Block(x, y, color=settings['block_color']))
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
                            pygame.mixer.music.load('app/assets/stone.mp3')
                            pygame.mixer.music.play()
                            self.blocks.remove(block)
                            self.score += 10

                # Проверка условий победы/поражения
                if len(self.blocks) == 0:
                    self.game_over = True
                    # Переход на следующий уровень
                    self.level_id += 1
                    pygame.mixer.music.load('app/assets/win.mp3')
                    pygame.mixer.music.play()
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
                        pygame.mixer.music.load('app/assets/game-over.mp3')
                        pygame.mixer.music.play()
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

            level_buttons = []

            for i in os.listdir('app/levels'):
                if i.endswith('.txt'):
                    level_id = int(i.split('.')[0])

                    # Создаем поверхность для кнопки
                    button_size = 50
                    level_surface = pygame.Surface((button_size, button_size))
                    level_surface.fill((100, 0, 0))  # Красный цвет

                    # Добавляем номер уровня
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(level_id), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(button_size / 2, button_size / 2))
                    level_surface.blit(text, text_rect)

                    def start_level(level_id):
                        global current_screen
                        with open('app/settings.json', 'r') as file:
                            old_data = json.load(file)
                        old_data['current_level'] = level_id
                        with open('app/settings.json', 'w') as file:
                            json.dump(old_data, file)
                        current_screen = Main(level_id)
                        current_screen.run()

                    # Размещаем кнопки в сетке, 12 в ряд
                    row = (level_id - 1) // 12
                    col = (level_id - 1) % 12
                    x = 100 + col * (button_size + 20)  # Отступ 20px
                    y = 100 + row * (button_size + 20)

                    level_button = Button(x, y, button_size, button_size, level_surface, start_level, level_id)
                    level_buttons.append(level_button)

            # Обрабатываем нажатия кнопок
            for e in level_buttons:
                screen.blit(e.surface, (e.x, e.y))
                e.process()

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

            screen.fill((50, 50, 50))

            # Создаем кнопки выбора цвета для блоков
            block_colors = [(255, 207, 64), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for i, color in enumerate(block_colors):
                color_surface = pygame.Surface((50, 50))
                color_surface.fill(color)

                def set_block_color(color):
                    with open('app/settings.json', 'r') as file:
                        data = json.load(file)
                    data['block_color'] = color
                    with open('app/settings.json', 'w') as file:
                        json.dump(data, file)

                color_button = Button(100 + i * 70, 100, 50, 50, color_surface, set_block_color, color)
                color_button.draw(screen)
                color_button.process()

            # Создаем кнопки выбора цвета для шарика
            ball_colors = [(255, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            for i, color in enumerate(ball_colors):
                color_surface = pygame.Surface((50, 50))
                color_surface.fill(color)

                def set_ball_color(color):
                    with open('app/settings.json', 'r') as file:
                        data = json.load(file)
                    data['ball_color'] = color
                    with open('app/settings.json', 'w') as file:
                        json.dump(data, file)

                color_button = Button(100 + i * 70, 200, 50, 50, color_surface, set_ball_color, color)
                color_button.draw(screen)
                color_button.process()

            # Создаем кнопки выбора цвета для платформы
            platform_colors = [(200, 200, 200), (150, 150, 150), (100, 100, 100), (50, 50, 50)]
            for i, color in enumerate(platform_colors):
                color_surface = pygame.Surface((50, 50))
                color_surface.fill(color)

                def set_platform_color(color):
                    with open('app/settings.json', 'r') as file:
                        data = json.load(file)
                    data['platform_color'] = color
                    with open('app/settings.json', 'w') as file:
                        json.dump(data, file)

                color_button = Button(100 + i * 70, 300, 50, 50, color_surface, set_platform_color, color)
                color_button.draw(screen)
                color_button.process()

            # Добавляем подписи
            font = pygame.font.Font(None, 36)
            block_text = font.render("Цвет блоков", True, (255, 255, 255))
            ball_text = font.render("Цвет шарика", True, (255, 255, 255))
            platform_text = font.render("Цвет платформы", True, (255, 255, 255))

            screen.blit(block_text, (100, 60))
            screen.blit(ball_text, (100, 160))
            screen.blit(platform_text, (100, 260))

            # Добавляем кнопку возврата на главный экран
            def back_to_main():
                global current_screen
                current_screen = Welcome()
                current_screen.run()

            back_surface = pygame.Surface((200, 50))
            back_surface.fill((100, 100, 100))
            back_text = font.render("Назад", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(center=(100, 25))
            back_surface.blit(back_text, back_text_rect)

            back_button = Button(300, 600, 200, 50, back_surface, back_to_main)
            back_button.draw(screen)
            back_button.process()

            pygame.display.update()
            clock.tick(1000 / Config.FPS)
