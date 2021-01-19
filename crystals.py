import random

import pygame
from load_image import load_image


class Crystal:
    def __init__(self, chunk):
        self.image = load_image('Images/base_crystal.png', 1)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.pos = (random.randint(0, chunk.width - 1), random.randint(0, chunk.width - 1))

    def render(self, chunk, screen):
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)


class HealthCrystal(Crystal):
    def __init__(self, chunk):
        super().__init__(chunk)
        self.image = load_image('Images/health.png', 1)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.food_count = 100

    def get_food(self):
        food = self.food_count
        self.food_count = 0
        return food


class FuelCrystal(Crystal):
    def __init__(self, chunk):
        super().__init__(chunk)
        self.image = load_image('Images/fuel.png', 1)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.fuel_count = 200

    def get_fuel(self):
        fuel = self.fuel_count
        self.fuel_count = 0
        return fuel
