import os
import sys

import pygame


# загрузка изображения
def load_image(path, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(path):
        print(f"Файл с изображением '{path}' не найден")
        sys.exit()
    image = pygame.image.load(path)
    return image
