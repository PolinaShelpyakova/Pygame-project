import json
import os.path
import sys
import pygame_gui

import pygame

WIDTH = 800
HEIGHT = 600
FPS = 30


class Hero(pygame.sprite.Sprite):
    character_go = ["images/go_r.png",
                    "images/stand.png",
                    "images/go_l.png",
                    "images/stand.png"]
    character_climb = ["images/climb_l.png",
                       "images/climb_r.png"]
    character_push = ["images/push_l.png",
                      "images/push_and_stand.png",
                      "images/push_r.png"]
    character_die = "images/die.png"
    character_jump = "images/jump.png"

    def __init__(self, pos, size=(50, 100)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.image = pygame.image.load(Hero.character_go[1]).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.go = False
        self.route = True
        self.frame_go = 0
        self.frame_climb = 0
        self.frame_push = 0
        self.flag = 0
        self.is_climb = False
        self.add(hero_sprites)
        self.is_hero_die = False

    def update(self, event=None):
        """
        Проверка событий.

        :return: None
        """
        if not self.is_hero_die:
            if event is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.go = True
                        self.route = True
                    elif event.key == pygame.K_LEFT:
                        self.go = True
                        self.route = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.go = False
                        self.route = True
                    elif event.key == pygame.K_LEFT:
                        self.go = False
                        self.route = False
            self.action('go', event)
            self.collide(event)
            self.jump(event)
            self.draw_health()
        else:
            self.go = False
            self.hero_died()

    def action(self, action, event):
        """
        Изменение картинки объекта в соответствии с выбранным действием.

        :param action: str
        :return: None
        """
        if action == 'die':
            self.image = pygame.image.load(Hero.character_die).convert_alpha()
        if action == 'jump':
            self.image = pygame.image.load(Hero.character_jump).convert_alpha()
        if action == 'climb':
            self.image = pygame.image.load(Hero.character_climb[self.frame_climb]).convert_alpha()
        if action == 'push':
            self.image = pygame.image.load(Hero.character_push[self.frame_push]).convert_alpha()
        if action == 'go':
            if self.go:
                if not self.route:
                    self.x -= 10
                else:
                    self.x += 10
                if self.flag == 1:
                    self.frame_go += 1
                if self.frame_go == 4:
                    self.frame_go = 0
                self.image = pygame.image.load(Hero.character_go[self.frame_go]).convert_alpha()
            else:
                self.image = pygame.image.load(Hero.character_go[1]).convert_alpha()
        if not self.route:
            self.image = pygame.transform.flip(self.image, True, False)
        if action != 'die':
            self.image = pygame.transform.scale(self.image, (50, 100))
        else:
            self.image = pygame.transform.scale(self.image, (100, 50))
        self.add(all_sprites)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.flag = 0 if self.flag == 1 else 1
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
                        event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if self.flag == 0:
                        self.frame_climb = 1 if self.frame_climb == 0 else 0
        if self.flag == 1:
            self.frame_push += 1
        if self.frame_push == 3:
            self.frame_push = 0

    def collide(self, event):
        """
        Столкновение с другими группами спрайтов.

        :return: None
        """
        if not pygame.sprite.spritecollideany(self, platform_sprites) and \
                not pygame.sprite.spritecollideany(self, ladder_sprites) and \
                not pygame.sprite.spritecollideany(self, box_sprites) and \
                not pygame.sprite.spritecollideany(self, acid_sprites):
            self.y += 10
            self.action('jump', event)
        if pygame.sprite.spritecollideany(self, ladder_sprites):
            if event is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.y += 10
                    if event.key == pygame.K_UP:
                        self.y -= 10
            self.action('climb', event)
            self.is_climb = True
        else:
            self.is_climb = False
        if pygame.sprite.spritecollideany(self, box_sprites) and pygame.sprite.spritecollideany(self, platform_sprites):
            self.action('push', event)
        if pygame.sprite.spritecollideany(self, acid_sprites) or pygame.sprite.spritecollideany(self, monster_sprites):
            self.action('die', event)
            self.is_hero_die = True

    def jump(self, event):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not self.is_climb:
                    if pygame.sprite.spritecollideany(self, platform_sprites) or \
                            pygame.sprite.spritecollideany(self, box_sprites):
                        self.y -= 50
                        self.action('jump', event)

    def draw_health(self):
        pass

    def hero_died(self):
        font_size = 100
        font = pygame.font.Font(None, font_size)
        font_color = (255, 0, 0)
        text = font.render('Hero died!', True, font_color)
        screen.blit(text, (80, 80))


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size=(100, 10)):
        super().__init__(all_sprites)
        self.pos = pos
        self.color = 'grey'
        self.size = size
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(platform_sprites)


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos, size=(10, 100)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.color = 'red'
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(ladder_sprites)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size=(10, 100)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.color = 'grey'
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(wall_sprites)


class Box(pygame.sprite.Sprite):
    def __init__(self, pos, size=(50, 50)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.color = 'white'
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(box_sprites)

    def update(self, event=None):
        self.collide()

    def collide(self):
        if not pygame.sprite.spritecollideany(self, platform_sprites) and \
                not pygame.sprite.spritecollideany(self, ladder_sprites) and \
                not pygame.sprite.spritecollideany(self, acid_sprites):
            self.rect = self.rect.move(self.vx, self.vy + 10)
        if pygame.sprite.spritecollideany(self, hero_sprites) and pygame.sprite.spritecollideany(self, platform_sprites)\
                or pygame.sprite.spritecollide(self, hero_sprites, False) and pygame.sprite.spritecollide(self, platform_sprites, False):
            if event is not None:
                if event.key == pygame.K_RIGHT:
                    self.push(True)
                if event.key == pygame.K_LEFT:
                    self.push(False)

    def push(self, route):
        if route:
            self.rect = self.rect.move(self.vx + 10, self.vy)
        else:
            self.rect = self.rect.move(self.vx - 10, self.vy)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos, size=(100, 50)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.color = 'white'
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(door_sprites)

    def update(self, event=None):
        if pygame.sprite.spritecollide(self, hero_sprites, False):
            open_level(2)


class Acid(pygame.sprite.Sprite):
    def __init__(self, pos, size=(100, 10)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.color = 'green'
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(acid_sprites)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, size=(20, 80)):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.color = 'pink'
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color(self.color), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], *self.size)
        self.vx = 0
        self.vy = 0
        self.add(monster_sprites)
        self.route = True

    def update(self, event=None):
        self.collide()

    def collide(self):
        if not pygame.sprite.spritecollideany(self, platform_sprites) and \
                not pygame.sprite.spritecollideany(self, ladder_sprites) and \
                not pygame.sprite.spritecollideany(self, acid_sprites) and \
                not pygame.sprite.spritecollideany(self, box_sprites):
            self.rect = self.rect.move(self.vx, self.vy + 10)
        elif pygame.sprite.spritecollideany(self, platform_sprites):
            if self.route:
                self.rect = self.rect.move(self.vx + 5, self.vy)
            else:
                self.rect = self.rect.move(self.vx - 5, self.vy)
        if pygame.sprite.spritecollide(self, ladder_sprites, False):
            self.route = True if not self.route else False
        if pygame.sprite.spritecollide(self, wall_sprites, False):
            self.route = True if not self.route else False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((255, 255, 255))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    start_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 300), (150, 50)),
        text='Начать игру',
        manager=manager
    )
    choice_level_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 400), (150, 50)),
        text='Карта уровней',
        manager=manager
    )
    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 500), (150, 50)),
        text='Настройки',
        manager=manager
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if start_game_btn.pressed:
                        open_level('1')
                    if choice_level_btn.pressed:
                        map_of_levels()
                    if settings_btn.pressed:
                        settings()
                    return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def map_of_levels():
    screen.fill((0, 255, 0))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 300), (150, 50)),
        text='В меню',
        manager=manager
    )
    level_btn1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0 * 100 + 100, 400), (50, 50)),
        text=f'{str(1)}',
        manager=manager
    )
    level_btn2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((1 * 100 + 100, 400), (50, 50)),
        text=f'{str(2)}',
        manager=manager
    )
    level_btn3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((2 * 100 + 100, 400), (50, 50)),
        text=f'{str(3)}',
        manager=manager
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if menu_btn.pressed:
                        start_screen()
                    if level_btn1.pressed:
                        open_level(level_btn1.text)
                    if level_btn2.pressed:
                        open_level(level_btn2.text)
                    if level_btn3.pressed:
                        open_level(level_btn3.text)
                    return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def settings():
    global pause
    screen.fill((0, 0, 255))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 300), (150, 50)),
        text='В меню',
        manager=manager
    )
    music_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 400), (150, 50)),
        text='Вкл/Выкл музыку',
        manager=manager
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if menu_btn.pressed:
                        start_screen()
                        return
                    if music_btn.pressed:
                        if not pause:
                            pygame.mixer.music.pause()
                            pause = True
                        elif pause:
                            pygame.mixer.music.unpause()
                            pause = False
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def final_screen():
    screen.fill((255, 255, 255))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    start_new_level_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 300), (150, 50)),
        text='Следующий уровень',
        manager=manager
    )
    menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 400), (150, 50)),
        text='В меню',
        manager=manager
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if menu_btn.pressed:
                        start_screen()
                        return
                    if start_new_level_btn.pressed:
                        return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def open_level(level):
    all_sprites.empty()
    direct = f'level_{str(level)}'
    for i in classes.keys():
        classes[i][1].empty()
    if os.path.exists(f'levels/{direct}.json'):
        with open(f'levels/{direct}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for objs in data:
                if objs != []:
                    for pos in objs:
                        classes[pos[0]][0](pos[1], pos[2])


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("music/song18.mp3")
    pygame.mixer.music.play(-1)
    pause = False
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True

    # Группы
    all_sprites = pygame.sprite.Group()
    hero_sprites = pygame.sprite.Group()
    platform_sprites = pygame.sprite.Group()
    ladder_sprites = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    acid_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    monster_sprites = pygame.sprite.Group()
    door_sprites = pygame.sprite.Group()

    classes = {'hero': [Hero, hero_sprites], 'platforms': [Platform, platform_sprites],
               'boxes': [Box, box_sprites], 'ladders': [Ladder, ladder_sprites],
               'acids': [Acid, acid_sprites], 'walls': [Wall, wall_sprites],
               'monster': [Monster, monster_sprites], 'door': [Door, monster_sprites, []]}
    start_screen()
    while running:
        is_update = True
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
            is_update = False
        if is_update:
            all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        if FLAG_NEXT_LVL:
            open_level(2)
    pygame.quit()
