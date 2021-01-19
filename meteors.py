from random import choice
import pygame
from load_image import load_image
import os
import random


# просто препятсвие
class Meteor:
    def __init__(self, chunk):
        positions = []
        for i in range(chunk.width):
            for j in range(chunk.height):
                if not chunk.board[i][j]:
                    positions.append((i, j))
        self.pos = choice(positions)
        self.image = load_image('Images/Meteors/' + random.choice(os.listdir('Images/Meteors')), 1)
        self.image = pygame.transform.scale(self.image, (90, 90))

    def render(self, chunk, screen):
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)
