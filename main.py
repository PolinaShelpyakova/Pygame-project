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

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.pos = pos
        self.image = pygame.image.load(Hero.character_go[1]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 100)
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
        self.current_health = 10
        self.max_health = 10
        self.dmg = 2
        self.add(hero_sprites)
        self.is_hero_die = False

    def update(self):
        """
        Проверка событий.

        :return: None
        """
        if not self.is_hero_die:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.go = True
                    self.route = True
                if event.key == pygame.K_LEFT:
                    self.go = True
                    self.route = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.go = False
                    self.route = True
                if event.key == pygame.K_LEFT:
                    self.go = False
                    self.route = False
            self.kill()
            self.action('go')
            self.collide()
            self.jump()
            self.draw_health()
        else:
            self.go = False
            self.hero_died()

    def action(self, action):
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
                    event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if self.flag == 0:
                    self.frame_climb = 1 if self.frame_climb == 0 else 0
        if self.flag == 1:
            self.frame_push += 1
        if self.frame_push == 3:
            self.frame_push = 0

    def collide(self):
        """
        Столкновение с другими группами спрайтов.

        :return: None
        """
        if not pygame.sprite.spritecollideany(self, platform_sprites) and \
                not pygame.sprite.spritecollideany(self, ladder_sprites) and \
                not pygame.sprite.spritecollideany(self, box_sprites) and \
                not pygame.sprite.spritecollideany(self, acid_sprites):
            self.y += 10
            self.action('jump')
        if pygame.sprite.spritecollideany(self, ladder_sprites):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.y += 10
                if event.key == pygame.K_UP:
                    self.y -= 10
            self.action('climb')
            self.is_climb = True
        else:
            self.is_climb = False
        if pygame.sprite.spritecollideany(self, box_sprites) and pygame.sprite.spritecollideany(self, platform_sprites):
            push_box = pygame.sprite.spritecollideany(self, box_sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    push_box.push(True)
                if event.key == pygame.K_LEFT:
                    push_box.push(False)
            self.action('push')
        if pygame.sprite.spritecollideany(self, acid_sprites):
            self.action('die')
            self.is_hero_die = True

    def jump(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not self.is_climb:
                if pygame.sprite.spritecollideany(self, platform_sprites) or \
                        pygame.sprite.spritecollideany(self, box_sprites):
                    self.y -= 50
                    self.action('jump')

    def draw_health(self):
        pass

    def hero_died(self):
        font_size = 100
        font = pygame.font.Font(None, font_size)
        font_color = (255, 0, 0)
        text = font.render('Hero died!', True, font_color)
        screen.blit(text, (80, 80))


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.pos = pos
        self.image = pygame.Surface((100, 10))
        pygame.draw.rect(self.image, pygame.Color("grey"), pygame.Rect(0, 0, 100, 10))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, 10)
        self.vx = 0
        self.vy = 0
        self.add(platform_sprites)


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.pos = pos
        self.image = pygame.Surface((10, 100))
        pygame.draw.rect(self.image, pygame.Color("red"), pygame.Rect(0, 0, 10, 100))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 10, 100)
        self.vx = 0
        self.vy = 0
        self.add(ladder_sprites)


class Box(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.pos = pos
        self.image = pygame.Surface((50, 50))
        pygame.draw.rect(self.image, pygame.Color("white"), pygame.Rect(0, 0, 50, 50))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 50)
        self.vx = 0
        self.vy = 0
        self.add(box_sprites)

    def update(self):
        self.collide()

    def collide(self):
        if not pygame.sprite.spritecollideany(self, platform_sprites) and \
                not pygame.sprite.spritecollideany(self, ladder_sprites) and \
                not pygame.sprite.spritecollideany(self, acid_sprites):
            self.rect = self.rect.move(self.vx, self.vy + 10)

    def push(self, route):
        if route:
            self.rect = self.rect.move(self.vx + 10, self.vy)
        else:
            self.rect = self.rect.move(self.vx - 10, self.vy)


class Acid(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.pos = pos
        self.image = pygame.Surface((100, 10))
        pygame.draw.rect(self.image, pygame.Color("green"), pygame.Rect(0, 0, 100, 10))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, 10)
        self.vx = 0
        self.vy = 0
        self.add(acid_sprites)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.pos = pos
        self.size = size
        self.image = pygame.Surface(self.size)
        pygame.draw.rect(self.image, pygame.Color("grey"), pygame.Rect(0, 0, *self.size))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, 10)
        self.vx = 0
        self.vy = 0
        self.add(wall_sprites)


class Monsters(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        pass


class SimpleMonster(Monsters):
    def __init__(self, pos):
        super().__init__(pos)
        self.pos = pos
        self.image = pygame.Surface((20, 80))
        pygame.draw.rect(self.image, pygame.Color("pink"), pygame.Rect(0, 0, 20, 80))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 20, 80)
        self.vx = 0
        self.vy = 0
        self.add(simple_monster_sprites)
        self.hp = 3
        self.dmg = 1
        self.route = True

    def update(self):
        self.collide()

    def collide(self):
        if not pygame.sprite.spritecollideany(self, platform_sprites) and \
                not pygame.sprite.spritecollideany(self, ladder_sprites) and \
                not pygame.sprite.spritecollideany(self, acid_sprites) and \
                not pygame.sprite.spritecollideany(self, box_sprites):
            self.rect = self.rect.move(self.vx, self.vy + 10)
        if pygame.sprite.spritecollideany(self, platform_sprites):
            if self.route:
                self.rect = self.rect.move(self.vx + 5, self.vy)
            else:
                self.rect = self.rect.move(self.vx - 5, self.vy)
        if pygame.sprite.spritecollideany(self, ladder_sprites) or pygame.sprite.spritecollideany(self, wall_sprites):
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
                        pass
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
    for i in range(3):
        level_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((i * 100 + 100, 400), (50, 50)),
            text=f'{str(i + 1)}',
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
                    if level_btn.pressed:
                        open_level(level_btn.text, None)
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


def open_level(level, hero):
    if event.key == pygame.K_2:
        if hero is not None:
            if hero.is_hero_die:
                level += 1
                final_screen()
        all_sprites.empty()
        direct = f'level_{str(level)}'
        for i in classes.keys():
            classes[i][1].empty()
            if os.path.exists(f'levels/{direct}/{i}.json'):
                with open(f'levels/{direct}/{i}.json', 'r') as file:
                    data = json.load(file)
                    for pos in data:
                        classes[i][1].add(classes[i][0](pos))
            else:
                final_screen()
                level = 1
        hero = None
    return level, hero


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("music/song18.mp3")
    pygame.mixer.music.play(-1)
    pause = False
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    color = (0, 0, 0)
    start_screen()
    running = True

    # Группы
    all_sprites = pygame.sprite.Group()
    hero_sprites = pygame.sprite.Group()
    platform_sprites = pygame.sprite.Group()
    ladder_sprites = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    acid_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    simple_monster_sprites = pygame.sprite.Group()

    classes = {'hero': [Hero, hero_sprites], 'platforms': [Platform, platform_sprites], 'boxes': [Box, box_sprites],
               'ladders': [Ladder, ladder_sprites], 'acids': [Acid, acid_sprites]}
    new_object = None  # Любой новый созданный объект можно двигать, кроме героя.
    level = 1
    hero = None
    while running:
        screen.fill(color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.KM & pygame.key.get_mods():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            new_object = Wall(event.pos, (100, 100))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and pygame.KMOD_SHIFT & pygame.key.get_mods():
                    new_object = Wall(event.pos, (10, 100))
                elif event.button == pygame.BUTTON_LEFT and pygame.KMOD_CTRL & pygame.key.get_mods():
                    new_object = Ladder(event.pos)
                elif event.button == pygame.BUTTON_RIGHT and pygame.KMOD_CTRL & pygame.key.get_mods():
                    new_object = Box(event.pos)
                elif event.button == pygame.BUTTON_MIDDLE and pygame.KMOD_CTRL & pygame.key.get_mods():
                    new_object = Acid(event.pos)
                elif event.button == pygame.BUTTON_RIGHT and not pygame.KMOD_CTRL & pygame.key.get_mods():
                    hero = Hero(event.pos)
                elif event.button == pygame.BUTTON_LEFT and not pygame.KMOD_CTRL & pygame.key.get_mods():
                    new_object = Platform(event.pos)
                elif event.button == pygame.BUTTON_MIDDLE and not pygame.KMOD_CTRL & pygame.key.get_mods():
                    new_object = SimpleMonster(event.pos)
            if event.type == pygame.KEYDOWN:
                if new_object:
                    if event.key == pygame.K_w:
                        new_object.rect.y -= 1
                    if event.key == pygame.K_s:
                        new_object.rect.y += 1
                    if event.key == pygame.K_a:
                        new_object.rect.x -= 1
                    if event.key == pygame.K_d:
                        new_object.rect.x += 1
                if event.key == pygame.K_1:
                    level = input('В какой уровень сохранить: ')
                    for i in classes.keys():
                        with open(f'levels/{level}/{i}.json', 'w') as file:
                            data = [sprite.rect.topleft for sprite in classes[i][1]]
                            json.dump(data, file)
                level, hero = open_level(level, hero)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

