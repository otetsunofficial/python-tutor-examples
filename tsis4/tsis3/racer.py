import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, color="Red"):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/sprite_racer.png").convert_alpha()
            # Уменьшим ширину до 45, чтобы машина выглядела стройнее и хитбокс был точнее
            self.image = pygame.transform.scale(self.original_image, (45, 80))
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill(pygame.Color(color))
            
        self.rect = self.image.get_rect(center=(200, 500))
        # СОЗДАЕМ МАСКУ для точных столкновений
        self.mask = pygame.mask.from_surface(self.image)
        
        self.base_speed = 5
        self.shield = False
        self.nitro_end_time = 0
        self.hp = 3

    def update(self, *args):
        keys = pygame.key.get_pressed()
        current_speed = self.base_speed * 1.8 if pygame.time.get_ticks() < self.nitro_end_time else self.base_speed
        
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.right < 400: self.rect.x += current_speed
        if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= current_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600: self.rect.y += current_speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/sprite_enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (45, 80))
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((200, 0, 0))
            
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -100))
        # СОЗДАЕМ МАСКУ для врага
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top > 600: self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(center=(random.randint(50, 350), -50))
        # Для простых фигур маска тоже полезна
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed=0, *args):
        move = speed if speed > 0 else (args[0] if args else 0)
        self.rect.y += move
        if self.rect.top > 600: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type
        self.image = pygame.Surface((30, 30))
        if p_type == "Nitro": self.image.fill((0, 0, 255))
        elif p_type == "Shield": self.image.fill((0, 255, 255))
        elif p_type == "Repair": self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, speed, *args):
        self.rect.y += speed
        if pygame.time.get_ticks() - self.spawn_time > 7000 or self.rect.top > 600:
            self.kill()