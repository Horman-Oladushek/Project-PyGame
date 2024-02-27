import os
import random
import sys
import pygame


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def error_screen():
    print('Не найден файл с картой')
    exit(0)


FPS = 50
SIZE = WIDTH, HEIGHT = 400, 500

pygame.init()
screen = pygame.display.set_mode(SIZE)

filename = input('Введите название файла: ')

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.jpg')
}
player_image = load_image('main_hero.png')

tile_width = tile_height = 50

try:
    level = load_level(filename)
except (FileNotFoundError, IOError):
    error_screen()


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Герой двигается,",
                  "Карта на месте", '',
                  'Для продолжения введите имя',
                  'файла с картой']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, all_sprites, walls_group)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, move_type: str):
        old = self.rect.copy()
        if move_type is not None:
            if move_type == 'right':
                self.rect.x += tile_width
            elif move_type == 'left':
                self.rect.x -= tile_width
            elif move_type == 'up':
                self.rect.y -= tile_height
            elif move_type == 'down':
                self.rect.y += tile_height
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect = old


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xp, yp = x, y
    # вернем игрока, а также размер поля в клетках
    new_player = Player(xp, yp)
    return new_player, x, y


if __name__ == '__main__':
    running = True
    fps = 30
    clock = pygame.time.Clock()
    camera = Camera()

    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    player, level_x, level_y = generate_level(load_level(filename))
    move_type = None

    start_screen()

    while running:
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                move_type = 'right'
            elif keys[pygame.K_LEFT]:
                move_type = 'left'
            elif keys[pygame.K_UP]:
                move_type = 'up'
            elif keys[pygame.K_DOWN]:
                move_type = 'down'
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.update(move_type)
        move_type = None
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
