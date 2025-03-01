import sys
import pygame
import pygame_gui
import random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("street fight")

rect = 10


def safe_records():
    with open('records.txt', 'r') as file:
        a = file.readline()
        file.close()

    return a


def exited():
    sys.exit()


def upload(path):
    try:
        return pygame.image.load(path)
    except FileNotFoundError:
        exited()


def upload_music(path):
    try:
        return pygame.mixer.Sound(path)
    except FileNotFoundError:
        exited()


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


status = 'menu'
while True:
    if status == 'menu':
        background1 = upload('images/background.png')
        background1 = pygame.transform.scale(background1, (1920, 1080))

        RULES = "<font face='verdana'>" \
                "СТРЕЛКИ - ПЕРЕДВИГАТСЯ" \
                "<br>WASD - ПЕРЕДВИГАТСЯ<font>" \
                "<br>ПРОБЕЛ-ПРЫЖОК<font>" \
                "<br>Q-УДАР НОГОЙ<font>" \
                "<br>E-УДАР РУКОЙ<font>" \
                "<br>B-БЛОК<font>"

        MENU_UPD = 0.016
        menu_main = pygame_gui.UIManager((1920, 1080))

        rules_box = pygame_gui.elements.UITextBox(
            html_text=RULES,
            relative_rect=pygame.Rect((835, 620), (250, 100)),
            manager=menu_main, visible=0)

        rules_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((835, 520), (250, 50)),
            text='Правила',
            manager=menu_main)
        start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((835, 470), (250, 50)),
            text='Старт',
            manager=menu_main)
        records_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((835, 570), (250, 50)),
            text='Рекорд',
            manager=menu_main)

        records_box = pygame_gui.elements.UITextBox(
            html_text="<font face='verdana'>" \
                      f'{safe_records()} секунд',
            relative_rect=pygame.Rect((835, 620), (250, 100)),
            manager=menu_main, visible=0)
        do = True
        while do:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exited()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start_button:
                            status = 'game'
                            rules_box.hide()
                            records_box.hide()
                            do = False
                        if event.ui_element == rules_button:
                            records_box.hide()
                            rules_box.show()
                        if event.ui_element == records_button:
                            rules_box.hide()
                            records_box.show()
                menu_main.process_events(event)
            screen.blit(background1, (0, 0))
            menu_main.update(MENU_UPD)
            menu_main.draw_ui(screen)
            pygame.display.update()


    elif status == 'game':
        pygame.mixer.music.load("sounds/background_music.mp3")
        status = 'play'
        background = upload('images/background1.png')
        background = pygame.transform.scale(background, (1920, 1080))
        time = 0
        idle = [upload('images/hero/idle/1.png'),
                upload('images/hero/idle/2.png'),
                upload('images/hero/idle/3.png')]

        block = [upload('images/hero/block/1.png')]

        hit = [upload('images/hero/hit/1.png'),
               upload('images/hero/hit/2.png'),
               upload('images/hero/hit/3.png'),
               upload('images/hero/hit/4.png')]

        jump = [upload('images/hero/jump/1.png'),
                upload('images/hero/jump/2.png'),
                upload('images/hero/jump/3.png'),
                upload('images/hero/jump/4.png'),
                upload('images/hero/jump/5.png'),
                upload('images/hero/jump/6.png')]

        kick = [upload('images/hero/kick/1.png'),
                upload('images/hero/kick/2.png'),
                upload('images/hero/kick/3.png'),
                upload('images/hero/kick/4.png'),
                upload('images/hero/kick/5.png')]

        punch = [upload('images/hero/punch/1.png'),
                 upload('images/hero/punch/2.png'),
                 upload('images/hero/punch/3.png'),
                 upload('images/hero/punch/4.png'),
                 upload('images/hero/punch/5.png')]

        walk = [upload('images/hero/walking/1.png'),
                upload('images/hero/walking/2.png'),
                upload('images/hero/walking/3.png'),
                upload('images/hero/walking/4.png'),
                upload('images/hero/walking/5.png')]

        eidle = [upload('images/enemy/idle/1.png'),
                 upload('images/enemy/idle/2.png'),
                 upload('images/enemy/idle/3.png'),
                 upload('images/enemy/idle/4.png')]

        ehit = [upload('images/enemy/hit/1.png'),
                upload('images/enemy/hit/2.png'),
                upload('images/enemy/hit/3.png'),
                upload('images/enemy/hit/4.png')]

        ekick = [upload('images/enemy/kick/1.png'),
                 upload('images/enemy/kick/2.png'),
                 upload('images/enemy/kick/3.png'),
                 upload('images/enemy/kick/4.png')]

        epunch = [upload('images/enemy/punch/1.png'),
                  upload('images/enemy/punch/2.png'),
                  upload('images/enemy/punch/3.png'),
                  upload('images/enemy/punch/4.png'),
                  upload('images/enemy/punch/5.png')]

        ewalk = [upload('images/enemy/walk/1.png'),
                 upload('images/enemy/walk/2.png'),
                 upload('images/enemy/walk/3.png'),
                 upload('images/enemy/walk/4.png'),
                 upload('images/enemy/walk/5.png')]

        idle_anim_count = 0
        walk_anim_count = 0
        jump_anim_count = 0
        kick_anim_count = 0
        punch_anim_count = 0
        hit_anim_count = 0

        eidle_anim_count = 0
        ewalk_anim_count = 0
        ekick_anim_count = 0
        epunch_anim_count = 0
        ehit_anim_count = 0
        side = 1
        x = 300
        y = 830
        win = upload_music("sounds/victory.mp3")
        punch_sound = upload_music("sounds/punch.mp3")
        pynch_block_sound = upload_music("sounds/punch_block.mp3")
        lost = upload_music("sounds/lost.mp3")


        class Enemy(pygame.sprite.Sprite):
            def __init__(self, player):
                super().__init__(all_sprites)
                self.hp = 100
                self.image = pygame.transform.scale(eidle[eidle_anim_count],
                                                    (180, 300))

                self.rect = self.image.get_rect(center=(player.rect.x + 1200, y))
                self.status = 'idle'
                self.mask = pygame.mask.from_surface(self.image)

            def idle(self):
                if enem.rect.x > player.rect.x:
                    self.image = pygame.transform.scale(eidle[round(eidle_anim_count / 20)],
                                                        (180, 300))

                    self.image = pygame.transform.flip(self.image, True, False)
                else:
                    self.image = pygame.transform.scale(eidle[round(eidle_anim_count / 20)],
                                                        (180, 300))

            def walk(self):
                if enem.rect.x > player.rect.x:
                    self.image = pygame.transform.scale(ewalk[round(ewalk_anim_count / 10)],
                                                        (180, 300))

                    self.image = pygame.transform.flip(self.image, True, False)
                else:

                    self.image = pygame.transform.scale(ewalk[round(ewalk_anim_count / 10)],
                                                        (180, 300))

            def kick(self):
                if enem.rect.x > player.rect.x:
                    if round(ekick_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(ekick[round(ekick_anim_count / 10)],
                                                            (270, 300))
                    else:
                        self.image = pygame.transform.scale(ekick[round(ekick_anim_count / 10)],
                                                            (180, 300))

                    self.image = pygame.transform.flip(self.image, True, False)
                else:
                    if round(ekick_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(ekick[round(ekick_anim_count / 10)],
                                                            (270, 300))
                    else:
                        self.image = pygame.transform.scale(ekick[round(ekick_anim_count / 10)],
                                                            (180, 300))

            def punch(self):
                if enem.rect.x > player.rect.x:
                    if round(epunch_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(epunch[round(epunch_anim_count / 10)],
                                                            (270, 300))

                    else:
                        self.image = pygame.transform.scale(epunch[round(epunch_anim_count / 10)],
                                                            (180, 300))

                    self.image = pygame.transform.flip(self.image, True, False)
                else:

                    if round(epunch_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(epunch[round(epunch_anim_count / 10)],
                                                            (270, 300))

                    else:
                        self.image = pygame.transform.scale(epunch[round(epunch_anim_count / 10)],
                                                            (180, 300))

            def hit(self):
                if enem.rect.x > player.rect.x:

                    self.image = pygame.transform.scale(ehit[round(ehit_anim_count / 10)],
                                                        (270, 300))
                    self.image = pygame.transform.flip(self.image, True, False)
                else:

                    self.image = pygame.transform.scale(ehit[round(ehit_anim_count / 10)],
                                                        (270, 300))


        class Hero(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__(all_sprites)
                self.image = pygame.transform.scale(idle[idle_anim_count],
                                                    (180, 300))
                self.hp = 100
                self.rect = self.image.get_rect(center=(x, y))
                self.status = 'idle'
                self.mask = pygame.mask.from_surface(self.image)

            def idle(self):
                if side == 1:
                    self.image = pygame.transform.scale(idle[round(idle_anim_count / 20)],
                                                        (180, 300))
                else:
                    self.image = pygame.transform.scale(idle[round(idle_anim_count / 20)],
                                                        (180, 300))
                    self.image = pygame.transform.flip(self.image, True, False)

            def walk(self):
                if side == 1:
                    self.image = pygame.transform.scale(walk[round(walk_anim_count / 10)],
                                                        (180, 300))
                else:
                    self.image = pygame.transform.scale(walk[round(walk_anim_count / 10)],
                                                        (180, 300))
                    self.image = pygame.transform.flip(self.image, True, False)

            def jump(self):
                if side == 1:
                    self.image = pygame.transform.scale(jump[round(jump_anim_count / 15)],
                                                        (180, 300))
                else:
                    self.image = pygame.transform.scale(jump[round(jump_anim_count / 15)],
                                                        (180, 300))
                    self.image = pygame.transform.flip(self.image, True, False)

            def kick(self):
                if side == 1:
                    if round(kick_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(kick[round(kick_anim_count / 10)],
                                                            (270, 300))
                    else:
                        self.image = pygame.transform.scale(kick[round(kick_anim_count / 10)],
                                                            (180, 300))
                else:
                    if round(kick_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(kick[round(kick_anim_count / 10)],
                                                            (270, 300))
                    else:
                        self.image = pygame.transform.scale(kick[round(kick_anim_count / 10)],
                                                            (180, 300))
                    self.image = pygame.transform.flip(self.image, True, False)

            def punch(self):
                if side == 1:
                    if round(punch_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(punch[round(punch_anim_count / 10)],
                                                            (270, 300))

                    else:
                        self.image = pygame.transform.scale(punch[round(punch_anim_count / 10)],
                                                            (180, 300))
                else:

                    if round(punch_anim_count / 10) == 2:
                        self.image = pygame.transform.scale(punch[round(punch_anim_count / 10)],
                                                            (270, 300))

                    else:
                        self.image = pygame.transform.scale(punch[round(punch_anim_count / 10)],
                                                            (180, 300))

                    self.image = pygame.transform.flip(self.image, True, False)

            def block(self):
                if side == 1:
                    self.image = pygame.transform.scale(block[0],
                                                        (180, 300))
                else:
                    self.image = pygame.transform.scale(block[0],
                                                        (180, 300))
                    self.image = pygame.transform.flip(self.image, True, False)

            def hit(self):
                if side == 1:

                    self.image = pygame.transform.scale(hit[round(hit_anim_count / 10)],
                                                        (270, 300))

                else:

                    self.image = pygame.transform.scale(hit[round(hit_anim_count / 10)],
                                                        (180, 300))

                    self.image = pygame.transform.flip(self.image, True, False)


        all_sprites = pygame.sprite.Group()
        player = Hero()
        enem = Enemy(player)
        do = True
        ss = 0
        pygame.mixer.music.play(-1)
        fx = 1510
        while do:
            if status == 'play':
                screen.blit(background, (0, 0))
                pygame.draw.rect(screen, 'red',
                                 (10, 10, player.hp * 4, 70))
                pygame.draw.rect(screen, 'red',
                                 (fx, 10, enem.hp * 4, 70))

                draw_text(screen, str(player.hp), 50, 70, 20)
                draw_text(screen, str(enem.hp), 50, 1850, 20)
                draw_text(screen, f'{round(time / 60)} sec', 100, 910, 0)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        do = False

                if enem.status == 'idle':
                    enem.rect.y = 750
                    if eidle_anim_count != 40:
                        eidle_anim_count += 1
                    else:
                        eidle_anim_count = 0
                    enem.idle()
                if enem.status == 'hit':
                    if ehit_anim_count != 30:
                        ehit_anim_count += 1
                    else:
                        ehit_anim_count = 0
                        enem.status = 'idle'
                    enem.hit()
                elif enem.status == 'walk':
                    enem.rect.y = 770
                    if ewalk_anim_count != 40:
                        ewalk_anim_count += 1
                    else:
                        ewalk_anim_count = 0
                    enem.walk()
                    if enem.rect.x == player.rect.x - 65 or enem.rect.x == player.rect.x + 65 or enem.rect.x < player.rect.x + 65 or enem.rect.x > player.rect.x - 65:
                        enem.status = 'idle'
                elif enem.status == 'kick':
                    enem.rect.y = 770
                    if ekick_anim_count != 30:
                        ekick_anim_count += 1

                    else:
                        enem.rect.y = 750
                        ekick_anim_count = 0
                        enem.status = 'idle'
                    enem.kick()
                elif enem.status == 'punch':
                    enem.rect.y = 770
                    if epunch_anim_count != 40:
                        epunch_anim_count += 1

                    else:
                        epunch_anim_count = 0
                        enem.rect.y = 750
                        enem.status = 'idle'
                    enem.punch()
                if enem.rect.y != 770 and enem.status != 'idle':
                    enem.rect.y += 5

                if enem.rect.x > player.rect.x + 120:
                    enem.rect.x -= 7
                    enem.status = 'walk'
                elif enem.rect.x < player.rect.x - 120:
                    enem.rect.x += 7
                    enem.status = 'walk'
                elif enem.rect.x == player.rect.x - 120 or enem.rect.x == player.rect.x + 120 or enem.rect.x < player.rect.x + 120 or enem.rect.x > player.rect.x - 120:
                    ss += 1
                    g = ['kick', 'punch']
                    if ss == 120:
                        enem.status = random.choice(g)
                        ss = 0
                else:
                    enem.status = 'idle'
                if player.rect.y != 770:
                    player.rect.y += 10
                    player.status = 'jump'

                else:
                    jump_anim_count = 0

                if player.status == 'walk':
                    if walk_anim_count != 40:
                        walk_anim_count += 1
                    else:
                        walk_anim_count = 0
                    player.walk()
                elif player.status == 'hit':
                    if hit_anim_count != 30:
                        hit_anim_count += 1
                    else:
                        hit_anim_count = 0
                        player.status = 'idle'
                    player.hit()
                elif player.status == 'jump':
                    if jump_anim_count != 75:
                        jump_anim_count += 1
                    else:
                        jump_anim_count = 0
                    player.jump()

                elif player.status == 'kick':
                    if kick_anim_count != 40:
                        kick_anim_count += 1
                    else:
                        kick_anim_count = 0
                        player.status = 'idle'
                    player.kick()

                elif player.status == 'punch':

                    if punch_anim_count != 40:
                        punch_anim_count += 1
                    else:
                        punch_anim_count = 0
                        player.status = 'idle'
                    player.punch()

                elif player.status == 'block':
                    player.block()

                else:
                    if idle_anim_count != 40:
                        idle_anim_count += 1
                    else:
                        idle_anim_count = 0
                    player.idle()

                if enem.status == 'punch' or enem.status == 'kick':
                    if player.status != 'block':
                        if pygame.sprite.collide_mask(enem, player):
                            if epunch_anim_count == 3 or ekick_anim_count == 3:
                                player.hp -= 10
                                punch_sound.play()
                                player.status = 'hit'
                    else:
                        if epunch_anim_count == 3 or ekick_anim_count == 3:
                            pynch_block_sound.play()
                if player.status == 'punch' or player.status == 'kick':
                    if pygame.sprite.collide_mask(player, enem):
                        if punch_anim_count == 3 or kick_anim_count == 3:
                            enem.hp -= 10
                            punch_sound.play()
                            fx += 40
                            enem.status = 'hit'

                if player.hp == 0 or enem.hp == 0:
                    if safe_records() == '':
                        with open('records.txt', 'w') as file:
                            file.write(str(round(time / 60)))
                            file.close()
                    elif int(safe_records()) > round(time / 60):
                        with open('records.txt', 'w') as file:
                            file.write(str(round(time / 60)))
                            file.close()
                    status = 'stop'

                key = pygame.key.get_pressed()

                if key[pygame.K_UP] or key[pygame.K_w] or key[pygame.K_SPACE]:
                    player.status = 'jump'
                    if player.rect.y == 770:
                        player.rect.y -= 400

                elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                    side = 1
                    player.status = 'walk'
                    if player.rect.x < 1750:
                        player.rect.x += 8

                elif key[pygame.K_LEFT] or key[pygame.K_a]:
                    side = 0
                    player.status = 'walk'
                    if player.rect.x > 0:
                        player.rect.x -= 8

                elif key[pygame.K_q]:
                    player.status = 'kick'

                elif key[pygame.K_e]:
                    player.status = 'punch'

                elif key[pygame.K_b]:
                    player.status = 'block'

                else:
                    if player.status != 'kick' and player.status != 'punch' and player.status != 'hit':
                        player.status = 'idle'
                all_sprites.draw(screen)
                all_sprites.update()
                pygame.display.update()
                time += 1
                clock.tick(60)
            else:
                pygame.mixer.music.pause()
                do = True
                time = 0
                if enem.hp == 0:
                    win.play()
                elif player.hp == 0:
                    lost.play()
                background1 = upload('images/background.png')
                background1 = pygame.transform.scale(background1, (1920, 1080))
                while do:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            do = False
                    screen.blit(background1, (0, 0))
                    if player.hp == 0:
                        draw_text(screen, 'Вы проиграли', 100, 960, 450)
                    elif enem.hp == 0:
                        draw_text(screen, 'Вы выйграли', 100, 960, 450)
                    time += 1
                    if round(time / 60) == 6:
                        do = False
                        status = 'menu'
                    pygame.display.update()
                    clock.tick(60)
    else:
        exited()