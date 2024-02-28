import pygame
import time
import sys
import os

pygame.init()

clock = pygame.time.Clock()
fps = 60
width = 900
height = 650
SIZE = width, height


gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("MAZE Game")


def load_image(name, colorkey=None):
    fullname = os.path.join('Data', name)
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


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.jpg'),
    'point': load_image('fon.jpg')
}
player_image = load_image('main_hero.png')
tile_width = 60
tile_height = 60
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(SIZE)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, all_sprites, walls_group)
        elif tile_type == 'empty':
            super().__init__(tiles_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites, point_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (60,60))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

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
    new_player, x, y, xp, yp = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 0:
                Tile('empty', x, y)
            elif level[y][x] == 1:
                Tile('wall', x, y)
            elif level[y][x] == 2:
                Tile('point', x, y)
            elif level[y][x] == 3:
                xp, yp = x, y
    # вернем игрока, а также размер поля в клетках
    new_player = Player(xp, yp)
    return new_player, x, y


def displayText(text):
    renderFont = pygame.font.Font('freesansbold.ttf', 45)

    textsc = renderFont.render(text, True, (255,255,255))

    surface, rect = textsc, textsc.get_rect()

    rect.center = ((width / 2), (height / 2))

    gameDisplay.blit(surface, rect)

    pygame.display.flip()
    all_sprites.draw(screen)
    player_group.draw(screen)

    time.sleep(1)

def move(key):
    global flag
    c = -1
    for i in maze:
        c += 1
        for j in i:
            if j == 3:
                y = c
                x = i.index(3)
    #Влево
    if key == 'left':
        block = maze[y][x - 1]
        if block == 0:
            maze[y][x - 1] = 3
            maze[y][x] = 0
            x = x - 1

        elif block == 2:
            maze[y][x - 1] = 3
            maze[y][x] = 0
            x = x - 1
            flag = True

    #Вправо
    if key == 'right':
        block = maze[y][x + 1]

        if block == 0:
            maze[y][x + 1] = 3
            maze[y][x] = 0
            x = x + 1
        elif block == 2:
            maze[y][x + 1] = 3
            maze[y][x] = 0
            x = x + 1
            flag = True


    #Вверх
    if key == 'up':
        block = maze[y - 1][x]
        if block == 0:
            maze[y - 1][x] = 3
            maze[y][x] = 0
            y = y - 1
        elif block == 2:
            maze[y - 1][x] = 3
            maze[y][x] = 0
            y = y - 1
            flag = True


    #Вниз
    if key == 'down':
        block = maze[y + 1][x]
        if block == 0:
            maze[y + 1][x] = 3
            maze[y][x] = 0
            y = y + 1
        elif block == 2:
            maze[y + 1][x] = 3
            maze[y][x] = 0
            y = y + 1
            flag = True

dest = None

# maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]

maze = [[1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 3, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1], ]

move_type = None
player, level_x, level_y = generate_level(maze)
flag = False
while True:
    generate_level(maze)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move('left')
                if flag is True:
                    dest = 1
            if event.key == pygame.K_RIGHT:
                move('right')
                if flag is True:
                    dest = 1
            if event.key == pygame.K_UP:
                move('up')
                if flag is True:
                    dest = 1
            if event.key == pygame.K_DOWN:
                a = move('down')
                if flag is True:
                    dest = 1
        if dest == 1:
            displayText("Yay! Level complete!")
            exit()

    all_sprites.update(move_type)
    move_type = None
    player_group.draw(screen)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
