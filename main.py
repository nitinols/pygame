import pygame
import sys
import math
import os

pygame.init()
pygame.mixer.init()
size = width, height = 1300, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tachanka')
FPS = 50
screen_rect = (0, 0, width, height)

SPAWNENEMI = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMI, 1000)

SPAWNENEMIBOSS = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMI, 10000)
YELLOW = (255, 255, 0)

def terminate():
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, width, height)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


arrow_image = load_image("arrow.png")
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
all_sprites = pygame.sprite.Group()
arrow_group = SpriteGroup()
enemy_group = SpriteGroup()
bullets_group = SpriteGroup()

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Arrow(Sprite):
    arrow = arrow_image
    arrow0 = []

    def __init__(self, pos):
        super().__init__(arrow_group)
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_arrow(position):
    Arrow(position)

def defeat():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    #pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').play()
    fon = pygame.transform.scale(load_image('gameover.jpg'), (800, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').stop()
                return
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                create_arrow(pygame.mouse.get_pos())
        screen.blit(fon, (0, 0))
        arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
        arrow_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    #pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').play(loops=-1)
    fon = pygame.transform.scale(load_image('fon.png'), size1)
    fon1 = pygame.transform.scale(load_image("fon2.png"), size1)
    screen.blit(fon, (0, 0))
    poss = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 570 <= event.pos[0] <= 700 and 130 <= event.pos[1] <= 180:
                    #pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').stop()
                    return
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                create_arrow(pygame.mouse.get_pos())
                if 570 <= event.pos[0] <= 700 and 130 <= event.pos[1] <= 170:
                    if not poss:
                        #pygame.mixer.Sound('D:/data/sounds/gunshot-dryfir.mp3').play()
                        poss = True
                    screen.blit(fon1, (0, 0))
                    create_arrow(pygame.mouse.get_pos())
                else:
                    poss = False
                    screen.blit(fon, (0, 0))
        arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
        arrow_group.draw(screen)
        if not poss:
            all_sprites.update()
            screen.blit(fon, (0, 0))
            arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
            arrow_group.draw(screen)
            all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

class Enemi(Sprite):
    def __init__(self, hp, sp, damag, pos, x, y):
        super().__init__(enemy_group)
        self.hp = hp
        self.speed = sp
        self.damag = damag
        self.sizen = 90, 150

        self.image = pygame.transform.scale(load_image("monstr2.png"), self.sizen)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.rect.x = x
        self.rect.y = y


    def update(self, player):
        dx, dy = self.rect.x - player.pos[0], self.rect.y - player.pos[1]
        if dx < 0:
            self.rect.x += self.speed
        elif dx > 0:
            self.rect.x -= self.speed
        if self.hp <= 0:
            self.kill()
        if not self.rect.colliderect(screen_rect):
            self.kill()


    def damages(self):
        self.hp -= 80

size_hero = 80, 120
player_image = pygame.transform.scale(load_image("player3.png"), size_hero)
player_image1 = pygame.transform.rotate(player_image, 180)
tile_width = 60
tile_height = 100
all_sprites_list = pygame.sprite.Group()

class Bullet(Sprite):

    def __init__(self, start_x, start_y, dest_x, dest_y):

        super().__init__(bullets_group)


        self.image = pygame.Surface([4, 10])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()

        self.rect.x = start_x
        self.rect.y = start_y

        self.floating_point_x = start_x
        self.floating_point_y = start_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        velocity = 10
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

    def update(self):

        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        if self.rect.x < 0 or self.rect.x > 1300 or self.rect.y < 0 or self.rect.y > 700:
            self.kill()

class Player(Sprite):
    def __init__(self, hp, sp, damag, pos, x, y):
        super().__init__(hero_group)
        self.image = pygame.transform.scale(load_image("player3.png"), (60, 100))
        self.heath = 500
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.rect.x = x
        self.rect.y = y
        self.yvel = 0
        self.xvel = 0
        self.onGround = False

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1])

    def get_damaged(self, damage):
        self.heath -= damage
        if self.heath <= 0:
            defeat()
            pygame.mixer.quit()
            pygame.mixer.init()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                    print('woooooooooooooooork')

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_list)
        self.image = pygame.Surface((1300, 50))
        self.image.fill(pygame.Color(YELLOW))
        self.image = pygame.transform.scale(load_image("start.png"), (1300, 70))
        self.rect = pygame.Rect(x, y, 1300, 50)




start_screen()
pygame.mixer.quit()
pygame.mixer.init()
GRAVITY = 0.35
running = True
enem = []
ongravity = False
bullets = []
pladform = Platform(0, 640)
screen = pygame.display.set_mode((1300, 700))
pf = []
pf.append(pladform)
camera = Camera()
hero = Player(200, 2, 8, (100, 540), 100, 540)
while running:
    for event in pygame.event.get():
        create_arrow(pygame.mouse.get_pos())
        if event.type == pygame.QUIT or hero.heath <= 0:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bul = Bullet(hero.rect.x + 10, hero.rect.y + 45, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
            all_sprites_list.add(bul)
            bullets.append(bul)
        if event.type == SPAWNENEMI:
            enem.append(Enemi(200, 1, 8, (100, 600), 100, 500))
            pass
    for j in enem:
            hit = pygame.sprite.spritecollide(j, bullets_group, True, pygame.sprite.collide_circle)
            if len(hit) != 0:
                j.damages()


    keys = pygame.key.get_pressed()
    x, y = hero.pos
    if hero.onGround == True and keys[pygame.K_SPACE]:
        x, y = hero.pos
        hero.move(x, y - 20)
        hero.yvel = -20
    if keys[pygame.K_LEFT] and x > 45:
        hero.move(x - 2, y)
    if keys[pygame.K_RIGHT] and x < 1300 - 45:
        hero.move(x + 2, y)
        hero_group.update(hero.pos[0], hero.pos[1])

    fon = pygame.transform.scale(load_image('fonmain.jpg'), (1300, 700))
    screen.blit(fon, (0, 0))
    intro_text = [f"Здоровье: {hero.heath}"]
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 1150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites_list.update()
    all_sprites.update()
    camera.update(hero)
    if not hero.onGround:
        hero.move(x, y + GRAVITY)
    bullets_group.update()
    arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])

    hero_group.update(hero.pos[0], hero.pos[1])
    hero_group.draw(screen)
    try:
        enemy_group.update(hero)
    except NameError:
        pass
    bullets_group.update()
    arrow_group.draw(screen)
    enemy_group.draw((screen))
    all_sprites.draw(screen)
    bullets_group.draw(screen)
    all_sprites_list.draw(screen)
    hero.collide(hero.xvel, hero.yvel, pf)
    clock.tick(FPS)
    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()