from app import screen
from config import Config
import pygame
import math
import json


class Button:
    """
    Класс для создания кнопок в игре
    """

    def __init__(self, x, y, width, height, surface, onclick, *args):
        # Координаты и размеры кнопки
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Изображение кнопки
        self.surface = surface
        # Функция обработки нажатия
        self.onclick = onclick
        self.args = args

        # Создаем прямоугольник для обработки коллизий
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        # Получаем позицию мыши
        mousePos = pygame.mouse.get_pos()

        # Проверяем нажатие на кнопку
        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.onclick(*self.args)

    def draw(self, screen):
        # Отрисовка кнопки
        screen.blit(self.surface, (self.x, self.y))


class Platform:
    """
    Класс платформы, которой управляет игрок
    """

    def __init__(self, x, y, width=Config.PLATFORM_WIDTH, height=Config.PLATFORM_HEIGHT):
        with open('app/settings.json', 'r') as file:
            settings = json.load(file)
        # Размеры платформы
        self.width = width
        self.height = height
        # Позиция платформы
        self.x = x - self.width // 2
        self.y = y
        # Скорость движения
        self.speed = Config.PLATFORM_SPEED
        # Прямоугольник для коллизий
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Цвет платформы
        self.color = settings['platform_color']

    def update(self):
        # Получаем нажатые клавиши
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Движение влево
        if keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)

        # Движение вправо
        if keys[pygame.K_RIGHT]:
            self.x = min(800 - self.width, self.x + self.speed)

        # Обновляем rect
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        # Отрисовка платформы
        pygame.draw.rect(screen, self.color, self.rect)


class Block:
    """
    Класс блоков, которые нужно разбивать
    """

    def __init__(self, x, y, width=Config.BLOCK_WIDTH, height=Config.BLOCK_HEIGHT, unbreakable=False, color=None):
        # Размеры блока
        self.width = width
        self.height = height
        # Позиция блока
        self.x = x
        self.y = y
        # Прямоугольник для коллизий
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.unbreakable = unbreakable
        # Цвет блока
        if color is None and not unbreakable:
            self.color = (255, 207, 64)
        elif color is None and unbreakable:
            self.color = (0, 0, 0)
        else:
            self.color = color

    def draw(self, screen):
        # Отрисовка блока
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    """
    Класс мяча, которым разбиваются блоки
    """

    def __init__(self, x, y):
        with open('app/settings.json', 'r') as file:
            settings = json.load(file)

        self.radius = Config.BALL_RADIUS
        self.x = x
        self.y = y

        self.speed_x = Config.BALL_SPEED
        self.speed_y = -Config.BALL_SPEED

        # Прямоугольник для коллизий
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)

        # Цвет мяча
        self.color = settings['ball_color']

        self.speed_up = False

    def update(self):
        print(self.x, self.y)

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        # Движение мяча
        self.x += self.speed_x
        self.y += self.speed_y

        # Ускорение
        if keys[pygame.K_SPACE] and not self.speed_up:
            self.speed_x *= 5
            self.speed_y *= 5
            self.speed_up = True
        elif self.speed_up:
            self.speed_x /= 5
            self.speed_y /= 5
            self.speed_up = False

        # Отскок от стен
        if self.x - self.radius <= 0:
            self.speed_x = abs(self.speed_x)
        if self.x + self.radius >= 800:
            self.speed_x = -abs(self.speed_x)
        if self.y - self.radius <= 0:
            self.speed_y = abs(self.speed_y)

        # Обновление rect
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        # Отрисовка мяча
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, obj):
        # Проверка столкновений с объектами
        if self.rect.colliderect(obj.rect):
            if isinstance(obj, Platform):
                self.speed_y *= -1
                # Изменяем угол отскока в зависимости от места удара
                relative_intersect_x = (obj.rect.x + obj.width / 2) - self.x
                normalized_intersect = relative_intersect_x / (obj.width / 2)
                bounce_angle = normalized_intersect * 60  # максимальный угол = 60 градусов
                self.speed_x = -Config.BALL_SPEED * math.sin(math.radians(bounce_angle))
                self.speed_y = -Config.BALL_SPEED * abs(math.cos(math.radians(bounce_angle)))

                if self.speed_up:
                    self.speed_x *= 5
                    self.speed_y *= 5
            else:  # для блоков
                self.speed_y *= -1
                return True
        return False

    def reset(self):
        # Сброс позиции и скорости мяча
        self.x = 400
        self.y = 530
        self.speed_x = 5
        self.speed_y = -5
