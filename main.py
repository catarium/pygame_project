import pygame
from map import Space
from GUI import Interface
from entities import Player
from load_image import load_image


def start_screen(screen):
    img = load_image('images/start.png')
    img_rect = img.get_rect()
    r = True
    while r:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.blit(img, img_rect)
        pygame.display.flip()
    pygame.quit()
    raise SystemExit


def end_screen(screen, text):
    screen.fill('black')
    font = pygame.font.Font(None, 80)
    text = font.render(text, True, pygame.Color('red'))
    text_x = screen.get_width() // 2
    text_y = screen.get_height() // 2
    r = True
    while r:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill('black')
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
    pygame.quit()
    raise SystemExit


def main():
    pygame.init()
    size = 900, 960
    screen = pygame.display.set_mode(size)
    start_screen(screen)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Game')
    space = Space()
    running = True
    interface = Interface()
    player = Player(space.chunks[space.current_chunk[0]][space.current_chunk[1]], 1000, 1000, 10, 1000, 100000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if player.fuel > 0:
                    if event.key == pygame.K_LEFT:
                        print('left')
                        if player.pos[0] == 0:
                            if space.current_chunk[1] == 0:
                                space.create_chunk('LEFT', space.current_chunk)
                                space.current_chunk = space.current_chunk
                                space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                    player.pos[1]] = None
                                player.pos = (9, player.pos[1])
                                player.n = len(space.chunks[space.current_chunk[0]][space.current_chunk[1]].objects)
                                space.chunks[space.current_chunk[0]][space.current_chunk[1]].objects.append(player)
                                player.pos = (9, player.pos[1])
                                player.image = pygame.transform.rotate(player.base_image, 90)
                            else:
                                space.current_chunk = (space.current_chunk[0], space.current_chunk[1] - 1)
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = None
                            player.pos = (9, player.pos[1])
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = player
                            player.image = pygame.transform.rotate(player.base_image, 90)
                        else:
                            player.move('LEFT', space.chunks[space.current_chunk[0]][space.current_chunk[1]])
                    elif event.key == pygame.K_RIGHT:
                        if player.pos[0] == 9:
                            if len(space.chunks[space.current_chunk[0]]) - 1 == space.current_chunk[1]:
                                space.create_chunk('RIGHT', space.current_chunk)
                            space.current_chunk = (space.current_chunk[0], space.current_chunk[1] + 1)
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = None
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = player
                            player.pos = (0, player.pos[1])
                            player.image = pygame.transform.rotate(player.base_image, -90)
                        else:
                            player.move('RIGHT', space.chunks[space.current_chunk[0]][space.current_chunk[1]])
                    elif event.key == pygame.K_UP:
                        if player.pos[1] == 0:
                            if space.current_chunk[0] == 0:
                                space.create_chunk('UP', space.current_chunk)
                                space.current_chunk = space.current_chunk
                            else:
                                space.current_chunk = (space.current_chunk[0] - 1, space.current_chunk[1])
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = None
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = player
                            player.pos = (player.pos[0], 9)
                            player.image = player.base_image
                        else:
                            player.move('UP', space.chunks[space.current_chunk[0]][space.current_chunk[1]])
                    elif event.key == pygame.K_DOWN:
                        if player.pos[1] == 9:
                            if space.current_chunk[0] == len(space.chunks) - 1:
                                space.create_chunk('DOWN', space.current_chunk)
                            space.current_chunk = (space.current_chunk[0] + 1, space.current_chunk[1])
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = None
                            space.chunks[space.current_chunk[0]][space.current_chunk[1]].board[player.pos[0]][
                                player.pos[1]] = player
                            player.pos = (player.pos[0], 0)
                            player.image = pygame.transform.rotate(player.base_image, 180)
                        else:
                            player.move('DOWN', space.chunks[space.current_chunk[0]][space.current_chunk[1]])
                if player.fuel != 0:
                    player.fuel -= player.fuel_consumption
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_chunk = space.chunks[space.current_chunk[0]][space.current_chunk[1]]
                player.shot(current_chunk, target=current_chunk.get_click(event.pos), screen=screen)
        if player.fuel <= 0 or player.health <= 0:
            if player.fuel <= 0:
                end_screen(screen, 'топливо закончилось')
            elif player.health <= 0:
                end_screen(screen, 'умер')
            size = 900, 960
            screen = pygame.display.set_mode(size)
            space = Space()
            interface = Interface()
            player = Player(space.chunks[space.current_chunk[0]][space.current_chunk[1]], 1000, 1000, 10, 1000, 100000)
        screen.fill(pygame.Color('black'))
        space.chunks[space.current_chunk[0]][space.current_chunk[1]].render(screen)
        interface.render(player.health, player.fuel, screen)
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()


if __name__ == '__main__':
    main()
