import pygame
from map import Board


class Interface:
    def __init__(self):
        pass

    def render(self, health, fuel, screen):
        font = pygame.font.Font(None, 40)
        text = font.render(f'Здоровье: {health} Топливо: {fuel}', True, (100, 255, 100))
        text_x = screen.get_width() // 100
        text_y = screen.get_height() - screen.get_height() // 100 * 4
        screen.blit(text, (text_x, text_y))


class Inventory(Board):
    def __init__(self, width, height, size):
        super().__init__(width, height)

    def render(self, screen, items):
        super.render(screen)
