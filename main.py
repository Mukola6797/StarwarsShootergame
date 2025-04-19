from random import randint

from pygame import *
from pygame.examples.blend_fill import data_dir

init()

WIDTH = 1000
HEIGHT = 800
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
missed_enemies = 0
killed_enemies = 0
mini_boss = None
last_boss_kills = 0
font.init()
font1 = font.SysFont('Arial', 36)
mini_boss = None
boss = None
mega_boss = None
last_mini_kills = 0
last_boss_kills = 0
last_mega_kills = 0

class Sprite:
    def __init__(self, x, y, width, height, img_path=None):
        self.img = img_path
        if self.img:
            self.img = transform.scale(image.load(img_path), (width, height))
            self.rect = self.img.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = Rect(x, y, width, height)

    # метод відображення спрайтів
    def reset(self):
        if self.img:
            window.blit(self.img, (self.rect.x, self.rect.y))
        else:
            draw.rect(window, (255, 0, 0), self.rect)

class Enemy(Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height, image_path)
        self.enemy_speed=2

    def movement(self, ):
        self.rect.y += self.enemy_speed

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 20) # Размеры пули 10x20
        self.speed = 12 # Скорость пули

    def update(self):
        self.rect.y -= self.speed  # Пуля летит вверх
        if self.rect.bottom < 0:  # Удаляем пулю, если она ушла за экран
            return True
        return False

class MiniBoss(Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height, image_path)
        self.hp = 20
        self.speed = 4

    def move(self):
        self.rect.y += self.speed

    def is_hit(self):
        self.hp -= 1
        return self.hp <= 0  # Возвращает True, если умер
class Boss(Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height, image_path)
        self.hp = 50
        self.speed = 2

    def move(self):
        self.rect.y += self.speed

    def is_hit(self):
        self.hp -= 1
        return self.hp <= 0


class MegaBoss(Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height, image_path)
        self.hp = 120
        self.speed = 1

    def move(self):
        self.rect.y += self.speed

    def is_hit(self):
        self.hp -= 1
        return self.hp <= 0

def update_player():
    keys = key.get_pressed()
    if keys[K_d]:
        player.rect.x += player_speed
    if keys[K_a]:
        player.rect.x -= player_speed

def update_player_with_mouse():
    mouse_x = mouse.get_pos()[0]
    player.rect.centerx = mouse_x
    #обмеження
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH

enemies = list()
for i in range(6):
    enemies.append(Enemy(randint(0, 900), randint(-600, -100), 150, 150, 'img/enemies/enemy.png'))
bullets = list()
player_speed = 7
player = Sprite(0, 650, 170, 150, 'img/player/player.png')
mini_boss = None
boss_spawned = False
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:  # Выстрел на SPACE
                bullet = Bullet(player.rect.centerx - 5, player.rect.top)
                bullets.append(bullet)
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:  # ЛКМ (Left Mouse Button)
                bullet = Bullet(player.rect.centerx - 5, player.rect.top)
                bullets.append(bullet)

    if killed_enemies % 25 == 0 and killed_enemies != 0 and (killed_enemies != last_boss_kills):
        mini_boss = MiniBoss(400, -200, 200, 200, r'img\enemies\mini_boss2.png')
        last_boss_kills = killed_enemies
        print(f"Появился минибосс! {killed_enemies} убийств.")

    if killed_enemies % 60 == 0 and killed_enemies != 0 and killed_enemies != last_boss_kills:
        boss = Boss(300, -250, 300, 300, r'img\enemies\Boss.png')
        last_boss_kills = killed_enemies

    if killed_enemies % 130 == 0 and killed_enemies != 0 and killed_enemies != last_mega_kills:
        mega_boss = MegaBoss(200, -300, 400, 400, r'img\enemies\MegaBoss.png')
        last_mega_kills = killed_enemies


    window.fill((0, 0, 0))
    player.reset()

    missed_text = font1.render(f"Пропущено: {missed_enemies}", True, (255, 255, 255))
    killed_text = font1.render(f"Вбито: {killed_enemies}", True, (255, 255, 255))
    window.blit(missed_text, (10, 10))
    window.blit(killed_text, (10, 70))


    for i in range(len(enemies)):
        enemies[i].reset()
        enemies[i].movement()

        if enemies[i].rect.top > HEIGHT:
            missed_enemies += 1
            enemies[i] = Enemy(randint(0, 900), -100, 150, 150, 'img/enemies/enemy.png')

    for bullet in bullets[:]:
        if bullet.update():
            bullets.remove(bullet)
        else:
            bullet.reset()

        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                enemies.remove(enemy)
                new_enemy = Enemy(randint(0, 900), randint(-600, -100), 150, 150, 'img/enemies/enemy.png')
                enemies.append(new_enemy)
                killed_enemies += 1
                break


        if mini_boss and bullet.rect.colliderect(mini_boss.rect):
            if bullet in bullets:
                bullets.remove(bullet)
            if mini_boss.is_hit():
                mini_boss = None


        if boss and bullet.rect.colliderect(boss.rect):
            if bullet in bullets:
                bullets.remove(bullet)
            if boss.is_hit():
                boss = None


        if mega_boss and bullet.rect.colliderect(mega_boss.rect):
            if bullet in bullets:
                bullets.remove(bullet)
            if mega_boss.is_hit():
                mega_boss = None


        if mini_boss and bullet.rect.colliderect(mini_boss.rect):
            if bullet in bullets:
                bullets.remove(bullet)
            if mini_boss.is_hit():
                mini_boss = None
    if mini_boss:
            mini_boss.reset()
            mini_boss.move()
            if mini_boss.rect.top > HEIGHT:
                mini_boss.rect.y = -mini_boss.rect.height
    if boss:
        boss.reset()
        boss.move()
        if boss.rect.top > HEIGHT:
            boss = None

    if mega_boss:
        mega_boss.reset()
        mega_boss.move()
        if mega_boss.rect.top > HEIGHT:
            mega_boss = None

    display.update()
    clock.tick(60)

    update_player()
    update_player_with_mouse()
