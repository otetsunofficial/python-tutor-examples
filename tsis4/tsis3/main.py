import pygame
import sys
import math
import random
# Импорт функций из твоих модулей
from persistence import load_settings, save_settings, save_score, load_leaderboard
from racer import Player, Enemy, Obstacle, PowerUp

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("racing game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Глобальные переменные и загрузка настроек
settings = load_settings()
username = ""
state = "USERNAME_INPUT"

def draw_text(text, x, y, color=(255, 255, 255), center=False):
    img = font.render(str(text), True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def game_loop():
    global state
    player = Player(settings["car_color"])
    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    distance = 0
    start_time = pygame.time.get_ticks()
    
    # События спавна
    ENEMY_EVENT = pygame.USEREVENT + 1
    POWERUP_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(ENEMY_EVENT, 1200)
    pygame.time.set_timer(POWERUP_EVENT, 5000)
    
    running = True
    while running:
        screen.fill((40, 40, 40)) 
        now = pygame.time.get_ticks()
        elapsed_sec = (now - start_time) / 1000
        
        # Формула сложности
        current_speed = 4 + math.log(1 + elapsed_sec/5) * math.sqrt(elapsed_sec * 0.25)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == ENEMY_EVENT:
                e = Enemy(current_speed)
                enemies.add(e)
                all_sprites.add(e)
                if random.random() < 0.3:
                    o = Obstacle()
                    obstacles.add(o)
                    all_sprites.add(o)
            
            if event.type == POWERUP_EVENT:
                ptype = random.choice(["Nitro", "Shield", "Repair"])
                p = PowerUp(ptype)
                powerups.add(p)
                all_sprites.add(p)

        # ПРОВЕРКА СТОЛКНОВЕНИЙ ПО МАСКАМ (Точная геометрия)
        # Ищем первого врага или препятствие, с которым столкнулся игрок
        hit_enemy = pygame.sprite.spritecollideany(player, enemies, pygame.sprite.collide_mask)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles, pygame.sprite.collide_mask)

        if hit_enemy or hit_obstacle:
            # Удаляем объект, в который врезались
            if hit_enemy: hit_enemy.kill()
            if hit_obstacle: hit_obstacle.kill()
            
            if player.shield:
                player.shield = False # Щит спасает
            else:
                player.hp -= 1
                if player.hp <= 0:
                    save_score(username, int(distance), distance)
                    state = "GAMEOVER"
                    running = False

        # Сбор бонусов (тоже по маске)
        collected = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_mask)
        for p in collected:
            if p.type == "Nitro":
                player.nitro_end_time = now + 4000 
            elif p.type == "Shield":
                player.shield = True
            elif p.type == "Repair":
                if player.hp < 3: player.hp += 1

        # Обновление
        player.update()
        enemies.update()
        obstacles.update(current_speed)
        powerups.update(current_speed)
        
        distance += current_speed / 10
        
        # Отрисовка
        pygame.draw.line(screen, (100, 100, 100), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
        all_sprites.draw(screen)
        
        # Интерфейс
        draw_text(f"Score: {int(distance)}", 10, 10, (255, 255, 0))
        for i in range(player.hp):
            pygame.draw.rect(screen, (255, 0, 0), (10 + (i * 25), 40, 20, 20))
            
        if now < player.nitro_end_time:
            t_rem = max(0, (player.nitro_end_time - now) // 1000)
            draw_text(f"NITRO: {t_rem}s", 10, 70, (0, 200, 255))
        if player.shield:
            draw_text("SHIELD ACTIVE", 10, 95, (0, 255, 255))

        pygame.display.flip()
        clock.tick(60)

# Главный цикл состояний
while True:
    screen.fill((25, 25, 25))
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if state == "USERNAME_INPUT":
        draw_text("ENTER YOUR NAME:", WIDTH//2, 250, center=True)
        draw_text(username, WIDTH//2, 300, color=(0, 255, 0), center=True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(username) > 0:
                    state = "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 12: username += event.unicode

    elif state == "MENU":
        draw_text("1. START RACE", WIDTH//2, 200, center=True)
        draw_text("2. SETTINGS", WIDTH//2, 250, center=True)
        draw_text("3. LEADERBOARD", WIDTH//2, 300, center=True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: state = "GAME"
                if event.key == pygame.K_2: state = "SETTINGS"
                if event.key == pygame.K_3: state = "LEADERBOARD"

    elif state == "SETTINGS":
        draw_text("SETTINGS", WIDTH//2, 100, color=(255, 255, 0), center=True)
        draw_text(f"C - Color: {settings['car_color']}", WIDTH//2, 200, center=True)
        draw_text(f"S - Sound: {'ON' if settings['sound'] else 'OFF'}", WIDTH//2, 250, center=True)
        draw_text("B - Save and Back", WIDTH//2, 350, color=(0, 255, 0), center=True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    cols = ["Red", "Blue", "Green", "Yellow"]
                    settings["car_color"] = cols[(cols.index(settings["car_color"]) + 1) % len(cols)]
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                if event.key == pygame.K_b:
                    save_settings(settings)
                    state = "MENU"

    elif state == "GAME":
        game_loop()

    elif state == "GAMEOVER":
        draw_text("GAME OVER", WIDTH//2, 250, color=(255, 0, 0), center=True)
        draw_text("Press M for Menu", WIDTH//2, 300, center=True)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                state = "MENU"

    elif state == "LEADERBOARD":
        lb = load_leaderboard()
        draw_text("TOP 10", WIDTH//2, 50, color=(255, 255, 0), center=True)
        for i, entry in enumerate(lb):
            draw_text(f"{i+1}. {entry['name']} - {entry['score']}", WIDTH//2, 100 + (i*35), center=True)
        draw_text("B - Back", WIDTH//2, 530, center=True)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                state = "MENU"

    pygame.display.flip()
    clock.tick(60)