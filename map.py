import random
from crystals import FuelCrystal, HealthCrystal
import pygame
from entities import Enemy, PlayerShell
from load_image import load_image
from meteors import Meteor


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[None] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 900 // width

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and cell < (self.width, self.height):
            return cell


# видимый кусок карты
class Chunk(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = load_image('Images/' + random.choice(('background.jpg', 'background2.jpg', 'background3.jpg',
                                                           'background4.jpg')))
        self.image = pygame.transform.scale(self.image, (900, 900))
        self.objects = []
        for _ in range(random.randint(1, 5)):
            crystal = random.choice((FuelCrystal(self), HealthCrystal(self)))
            self.board[crystal.pos[0]][crystal.pos[1]] = crystal
        for _ in range(random.randint(1, 5)):
            meteor = Meteor(self)
            self.board[meteor.pos[0]][meteor.pos[1]] = meteor
        for _ in range(random.randint(1, 4)):
            enemy = Enemy(self)
            self.board[enemy.pos[0]][enemy.pos[1]] = enemy

    def render(self, screen):
        super().render(screen)
        screen.blit(self.image, (0, 0))
        objects = []
        for i in self.board:
            objects += i
        objects = [i for i in objects if i]
        for i in objects:
            i.render(self, screen)


# вся карта
class Space:
    def __init__(self):
        self.chunks = [[Chunk(10, 10)]]
        self.current_chunk = (0, 0)

    def create_chunk(self, direction):
        if direction == 'UP':
            self.chunks.insert(0, [Chunk(10, 10) for _ in range(len(self.chunks[self.current_chunk[0]]))])
        elif direction == 'DOWN':
            self.chunks.append([Chunk(10, 10) for _ in range(len(self.chunks[self.current_chunk[0]]))])
        elif direction == 'RIGHT':
            for i in range(len(self.chunks)):
                self.chunks[i].append(Chunk(10, 10))
        elif direction == 'LEFT':
            for i in range(len(self.chunks)):
                self.chunks[i].insert(0, Chunk(10, 10))
