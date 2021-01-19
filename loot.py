import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class HealthUpgrade:
    def __init__(self, value, pos):
        self.value = value
        self.image = load_image('health_update.png')
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.pos = pos

    def render(self, chunk, screen):
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)


class FuelUpgrade:
    def __init__(self, value, pos):
        self.value = value
        self.image = load_image('fuel_upgrade.png')
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.pos = pos

    def render(self, chunk, screen):
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)
