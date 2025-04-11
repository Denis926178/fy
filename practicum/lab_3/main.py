import pygame
import sys
import random
import time

import asyncio

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игра v1.0")

fon = pygame.image.load('fon.jpg')
fon = pygame.transform.scale(fon, (window_width, window_height))

async def redraw_enemy(all_sprites, enemies):
    print("Im here")
    await asyncio.sleep(2)

    enemy = Enemy(window_width, random.randint(0, window_height - 50))
    all_sprites.add(enemy)
    enemies.add(enemy)

class Player(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x=100, hero_y=250, speed_x=5, speed_y=5):
        super().__init__()
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.rect = self.image.get_rect()
        self.rect.x = hero_x
        self.rect.y = hero_y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed_y
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width:
            self.rect.right = window_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > window_width:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, 3)
        self.last_spawn_time = time.time()

    def update(self):
        """Перемещает врага"""
        self.rect.x -= self.speed
        if self.rect.right < 0:
            current_time = time.time()
            if current_time - self.last_spawn_time > 10:
                self.rect.x = window_width
                self.last_spawn_time = current_time

async def main():
    filename = 'player.png'
    hero = Player(filename)
    enemy1 = Enemy(700, random.randint(0, window_height - 50))
    enemy2 = Enemy(700, random.randint(0, window_height - 50))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(enemy1)
    all_sprites.add(enemy2)

    enemies = pygame.sprite.Group()
    enemies.add(enemy1)
    enemies.add(enemy2)

    arrows = pygame.sprite.Group()

    speed_x = 0
    speed_y = 0
    dist_fon_x = 0
    dist_fon_y = 0
    last_enemy_spawn_time = time.time()

    running = True
    clock = pygame.time.Clock()
    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arrow = Arrow(hero.rect.right, hero.rect.centery)
                    all_sprites.add(arrow)
                    arrows.add(arrow)

        keys = pygame.key.get_pressed()
        hero.update(keys)
        arrows.update()
        enemies.update()

        if hero.rect.left <= 0 and keys[pygame.K_LEFT]:
            speed_x = 5
        elif hero.rect.right >= window_width and keys[pygame.K_RIGHT]:
            speed_x = -5
        else:
            speed_x = 0

        dist_fon_x = (dist_fon_x + speed_x) % window_width
        dist_fon_y = (dist_fon_y + speed_y) % window_height

        window.blit(fon, (dist_fon_x, dist_fon_y))
        if dist_fon_x != 0:
            window.blit(fon, (dist_fon_x - window_width, dist_fon_y))
        if dist_fon_y != 0:
            window.blit(fon, (dist_fon_x, dist_fon_y - window_height))
        if dist_fon_x != 0 and dist_fon_y != 0:
            window.blit(fon, (dist_fon_x - window_width, dist_fon_y - window_height))

        collisions = pygame.sprite.groupcollide(arrows, enemies, True, False)  # Не удаляем врагов сразу

        for arrow, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                enemy.kill()
                asyncio.create_task(redraw_enemy(all_sprites, enemies))

        all_sprites.draw(window)

        pygame.display.update()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
