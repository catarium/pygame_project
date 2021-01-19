import os
import sys
import pygame
from load_image import load_image


# бонус к здоровью
class HealthUpgrade:
    def __init__(self, value, pos):
        self.value = value
        self.image = load_image('images/health_update.png')
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.pos = pos

    def render(self, chunk, screen):
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)


# бонус к топливу
class FuelUpgrade:
    def __init__(self, value, pos):
        self.value = value
        self.image = load_image('images/fuel_upgrade.png')
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.pos = pos

    def render(self, chunk, screen):
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)
