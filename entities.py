import random
from load_image import load_image
import pygame
from crystals import HealthCrystal, FuelCrystal, Crystal
from loot import HealthUpgrade, FuelUpgrade
from meteors import Meteor


class Entity:
    def __init__(self, chunk):
        while True:
            pos = (random.randint(0, 9), random.randint(0, 9))
            if not chunk.board[pos[0]][pos[1]]:
                self.pos = pos
                break
        chunk.board[self.pos[0]][self.pos[1]] = self
        self.heath = 1000000
        self.fuel = 1000000
        self.image = load_image('Images/RD1.png', 1)

    def move(self):
        pass

    def render(self, chunk, screen):
        chunk.board[self.pos[0]][self.pos[1]] = self


class Player(Entity):
    def __init__(self, chunk, max_health, max_fuel, fuel_consumption, health, fuel):
        super().__init__(chunk)
        self.max_health = max_health
        self.max_fuel = max_fuel
        self.fuel_consumption = fuel_consumption
        self.health = health
        self.fuel = fuel
        self.image = load_image('Images/spaceship.png', 1)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.base_image = self.image.copy()
        chunk.board[self.pos[0]][self.pos[1]] = self

    def move(self, direction, chunk):
        super().move()
        chunk.board[self.pos[0]][self.pos[1]] = None
        old_pos = self.pos
        if direction == 'LEFT':
            self.pos = (self.pos[0] - 1, self.pos[1])
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif direction == 'RIGHT':
            self.pos = (self.pos[0] + 1, self.pos[1])
            self.image = pygame.transform.rotate(self.base_image, -90)
        elif direction == 'UP':
            self.pos = (self.pos[0], self.pos[1] - 1)
            self.image = self.base_image
        elif direction == 'DOWN':
            self.pos = (self.pos[0], self.pos[1] + 1)
            self.image = pygame.transform.rotate(self.base_image, 180)
        if type(chunk.board[self.pos[0]][self.pos[1]]) == HealthCrystal:
            self.health += 50
            chunk.board[self.pos[0]][self.pos[1]] = None
        elif type(chunk.board[self.pos[0]][self.pos[1]]) == FuelCrystal:
            self.fuel += chunk.board[self.pos[0]][self.pos[1]].get_fuel()
            chunk.board[self.pos[0]][self.pos[1]] = None
        elif type(chunk.board[self.pos[0]][self.pos[1]]) == Enemy:
            self.health -= 100
            chunk.board[self.pos[0]][self.pos[1]] = None
        elif type(chunk.board[self.pos[0]][self.pos[1]]) == HealthUpgrade:
            self.max_health += chunk.board[self.pos[0]][self.pos[1]].value
        elif type(chunk.board[self.pos[0]][self.pos[1]]) == FuelUpgrade:
            self.max_fuel += chunk.board[self.pos[0]][self.pos[1]].value
        elif type(chunk.board[self.pos[0]][self.pos[1]]) == Meteor:
            self.pos = old_pos
        if self.health > self.max_health:
            self.health = self.max_health
        if self.fuel > self.max_fuel:
            self.fuel = self.max_fuel
        chunk.board[self.pos[0]][self.pos[1]] = self

    def render(self, chunk, screen):
        super().render(chunk, screen)
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2, chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)

    def shot(self, chunk, target, screen):
        shell = PlayerShell(chunk, (self.pos[0], self.pos[1]), target, screen=screen)
        super().render(chunk, screen)


class Enemy(Entity):
    def __init__(self, chunk):
        super().__init__(chunk)
        self.image = load_image('Images/enemy.png', 1)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.base_image = self.image.copy()
        self.last_tick = -1
        self.drop = random.choice((HealthUpgrade(100, self.pos), FuelUpgrade(100, self.pos)))
        self.killed = False
        self.last_shot = -1

    def move(self, chunk, x2, y2, screen):
        x1, y1 = self.pos
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= chunk.width or y + dy < 0 or y + dy >= chunk.height:
                        continue
                    if not chunk.board[x + dx][y + dy] or (y + dy, x + dx) == (y2, x2):
                        dn = d.get((x + dx, y + dy), -1)
                        if dn > d.get((x, y), -1) + 1 or dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        path = []
        if dist >= 0:
            v = []
            path = [((x2, y2), dist)]
            while path[-1][-1] != 0:
                x2, y2 = path[-1][0]
                for dy in range(-1, 2):
                    v.append(((x2 + dy, y2), d.get((x2 + dy, y2), chunk.width * chunk.height)))
                    v.append(((x2, y2 + dy), d.get((x2, y2 + dy), chunk.width * chunk.height)))

                path.append(min(v, key=lambda a: a[1]))
                v = []

        return path

    def render(self, chunk, screen):
        if self.killed:
            img = load_image('Images/explosion.png', 1)
            img = pygame.transform.scale(img, (90, 90))
            img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                                   chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
            screen.blit(img, img_rect)
            self.drop.pos = self.pos
            chunk.board[self.pos[0]][self.pos[1]] = self.drop
        else:
            if self.last_tick == -1 or pygame.time.get_ticks() - self.last_tick >= 250 and (self.last_shot == -1 or pygame.time.get_ticks() - self.last_shot >= 600):
                x2, y2 = self.pos
                for i in chunk.board:
                    for j in i:
                        if type(j) == Player:
                            x2, y2 = j.pos
                if x2 == self.pos[0] or y2 == self.pos[1]:
                    chunk.board[self.pos[0]][self.pos[1]] = self
                    flag = False
                    direction = ''
                    if x2 > self.pos[0]:
                        if len(set([chunk.board[i][self.pos[1]] for i in range(self.pos[0], x2)])) <= 2:
                            direction = 'RIGHT'
                            flag = True
                    elif x2 < self.pos[0]:
                        if len(set([chunk.board[i][self.pos[1]] for i in range(self.pos[0], x2, -1)])) <= 2:
                            direction = 'LEFT'
                            flag = True
                    elif y2 > self.pos[1]:
                        if len(set([chunk.board[self.pos[0]][i] for i in range(self.pos[1], y2)])) <= 2:
                            flag = True
                            direction = 'DOWN'
                    elif y2 < self.pos[1]:
                        if len(set([chunk.board[self.pos[0]][i] for i in range(self.pos[1], y2, -1)])) <= 2:
                            flag = True
                            direction = 'UP'
                    if self.last_shot == -1 or pygame.time.get_ticks() - self.last_shot >= 1000:
                        EnemyShell(direction, self.pos, chunk, screen, self)
                        self.last_shot = pygame.time.get_ticks()
                    img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                                           chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
                    screen.blit(self.image, img_rect)
                    self.last_tick = pygame.time.get_ticks()
                    if flag:
                        return
                    else:
                        print('No')
                # try:
                try:
                    path = self.move(chunk, x2, y2, screen)[-2]
                except IndexError:
                    path = (self.pos, None)
                # except IndexError as e:
                #     print(self.move(chunk, x2, y2, screen))
                #     return
                chunk.board[self.pos[0]][self.pos[1]] = None
                old_pos = self.pos
                self.pos = path[0]
                if type(chunk.board[self.pos[0]][self.pos[1]]) == Player:
                    chunk.board[self.pos[0]][self.pos[1]].health -= 100
                else:
                    if old_pos[0] > self.pos[0]:
                        self.image = pygame.transform.rotate(self.base_image, 90)
                    elif old_pos[0] < self.pos[0]:
                        self.image = pygame.transform.rotate(self.base_image, -90)
                    elif old_pos[1] > self.pos[1]:
                        self.image = self.base_image
                    elif old_pos[1] < self.pos[1]:
                        self.image = self.image = pygame.transform.rotate(self.base_image, 180)
                    chunk.board[self.pos[0]][self.pos[1]] = self
                img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                                       chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
                screen.blit(self.image, img_rect)
                self.last_tick = pygame.time.get_ticks()
            else:
                img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                                       chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
                screen.blit(self.image, img_rect)


class EnemyShell(Entity):
    def __init__(self, direction, pos, chunk, screen, enemy):
        self.pos = pos
        self.direction = direction
        self.last_step = -1
        self.image = load_image('Images/enemy_rocket.png', 1)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.base_image = self.image.copy()
        self.render(chunk, screen)
        chunk.board[pos[0]][pos[1]] = enemy

    def render(self, chunk, screen):
        if self.last_step == -1 or pygame.time.get_ticks() - self.last_step >= 200:
            try:
                chunk.board[self.pos[0]][self.pos[1]] = None
                old_pos = self.pos
                if self.direction == 'UP':
                    self.image = self.base_image
                    self.pos = (self.pos[0], self.pos[1] - 1)
                elif self.direction == 'DOWN':
                    self.image = pygame.transform.rotate(self.base_image, 180)
                    self.pos = (self.pos[0], self.pos[1] + 1)
                elif self.direction == 'RIGHT':
                    self.image = pygame.transform.rotate(self.base_image, -90)
                    self.pos = (self.pos[0] + 1, self.pos[1])
                elif self.direction == 'LEFT':
                    self.image = pygame.transform.rotate(self.base_image, 90)
                    self.pos = (self.pos[0] - 1, self.pos[1])
                if not isinstance(chunk.board[self.pos[0]][self.pos[1]], type(None)):
                    if type(chunk.board[self.pos[0]][self.pos[1]]) == Player:
                        chunk.board[self.pos[0]][self.pos[1]].health -= 50
                else:
                    chunk.board[self.pos[0]][self.pos[1]] = self

            except IndexError:
                chunk.board[old_pos[0]][old_pos[1]] = None
            self.last_step = pygame.time.get_ticks()
        img_rect = self.image.get_rect(center=(chunk.cell_size * (self.pos[0] + 1) - chunk.cell_size // 2,
                                               chunk.cell_size * (self.pos[1] + 1) - chunk.cell_size // 2))
        screen.blit(self.image, img_rect)


class PlayerShell(Entity):
    def __init__(self, chunk, start, target, screen):
        try:
            self.target = target
            self.pos = start
            self.path = self.move(chunk, screen)
            self.pos = self.path.pop(-1)[0]
            self.color = pygame.Color('yellow')
            self.render(chunk, screen)
        except IndexError:
            return
        except TypeError:
            return

    def move(self, chunk, screen):
        x1, y1 = self.pos
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= chunk.width or y + dy < 0 or y + dy >= chunk.height:
                        continue
                    dn = d.get((x + dx, y + dy), -1)
                    if dn > d.get((x, y), -1) + 1 or dn == -1:
                        d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                        v.append((x + dx, y + dy))
        x2, y2 = self.target
        dist = d.get((x2, y2), -1)
        path = []
        if dist >= 0:
            v = []
            path = [((x2, y2), dist)]
            while path[-1][-1] != 0:
                x2, y2 = path[-1][0]
                for dy in range(-1, 2):
                    v.append(((x2 + dy, y2), d.get((x2 + dy, y2), chunk.width * chunk.height)))
                    v.append(((x2, y2 + dy), d.get((x2, y2 + dy), chunk.width * chunk.height)))

                path.append(min(v, key=lambda a: a[1]))
                v = []
        return path

    def render(self, chunk, screen):
        try:
            # for i in chunk.board:
            #     print(i)
            # print()
            chunk.board[self.pos[0]][self.pos[1]] = None
            pygame.draw.ellipse(screen, pygame.Color("yellow"),
                                (self.pos[0] * chunk.cell_size + chunk.left,
                                 self.pos[1] * chunk.cell_size + chunk.top, chunk.cell_size,
                                 chunk.cell_size))
            self.pos = self.path.pop(-1)[0]
            if chunk.board[self.pos[0]][self.pos[1]]:
                if type(chunk.board[self.pos[0]][self.pos[1]]) == Enemy:
                    chunk.board[self.pos[0]][self.pos[1]].killed = True
                else:
                    chunk.board[self.pos[0]][self.pos[1]] = None
            else:
                chunk.board[self.pos[0]][self.pos[1]] = self
            # c = 0
            # for i in chunk.board:
            #     for j in i:
            #         if type(j) == PlayerShell:
            #             c += 1
        except IndexError:
            chunk.board[self.pos[0]][self.pos[1]] = None
