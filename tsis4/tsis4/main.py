import pygame
import random
from db import DB
from config import load_settings, save_settings

WIDTH, HEIGHT, CELL = 800, 600, 20

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.db = DB()
        self.settings = load_settings()
        self.font = pygame.font.SysFont("Arial", 22)
        self.state = "MENU"
        self.username = "robloxgod"
        self.reset_game()

    def reset_game(self):
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.dir = [CELL, 0]
        self.score, self.level, self.speed = 0, 1, 10
        self.obstacles = []
        self.food = self.spawn_item()
        self.poison = self.spawn_item()
        self.powerup = None # [pos, type, spawn_time]
        self.shield = False
        self.effect_end = 0
        self.p_id, self.best = None, 0

    def spawn_item(self):
        while True:
            pos = [random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL)]
            if pos not in self.snake and pos not in self.obstacles: return pos

    def update(self):
        now = pygame.time.get_ticks()
        # Эффекты бонусов
        if self.effect_end and now > self.effect_end:
            self.speed = 10 + (self.level - 1) * 2
            self.effect_end = 0

        # Спавн бонуса раз в 15 сек
        if not self.powerup and random.random() < 0.01:
            self.powerup = [self.spawn_item(), random.choice(["SPEED", "SLOW", "SHIELD"]), now]

        # Исчезновение бонуса через 8 сек
        if self.powerup and now - self.powerup[2] > 8000:
            self.powerup = None

        head = [self.snake[0][0] + self.dir[0], self.snake[0][1] + self.dir[1]]
        
        # Столкновения
        hit = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in self.snake or head in self.obstacles
        if hit:
            if self.shield: self.shield = False; self.snake.pop()
            else: self.db.save_result(self.p_id, self.score, self.level); self.state = "GAMEOVER"; return
        
        self.snake.insert(0, head)

        if head == self.food:
            self.score += 10
            self.food = self.spawn_item()
            if self.score % 30 == 0:
                self.level += 1; self.speed += 2
                if self.level >= 3: self.obstacles.append(self.spawn_item()) #
        elif head == self.poison: #
            self.poison = self.spawn_item()
            if len(self.snake) > 2: self.snake.pop(); self.snake.pop()
            else: self.state = "GAMEOVER"
        elif self.powerup and head == self.powerup[0]: #
            p_type = self.powerup[1]
            if p_type == "SPEED": self.speed += 5; self.effect_end = now + 5000
            elif p_type == "SLOW": self.speed = max(5, self.speed - 5); self.effect_end = now + 5000
            elif p_type == "SHIELD": self.shield = True
            self.powerup = None
        else:
            self.snake.pop()

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def draw(self):
        self.screen.fill((20, 20, 20))
        if self.settings["grid"]: #
            for x in range(0, WIDTH, CELL): pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        
        for s in self.snake: pygame.draw.rect(self.screen, self.settings["snake_color"], (*s, CELL-1, CELL-1))
        if self.shield: pygame.draw.rect(self.screen, (255, 255, 255), (*self.snake[0], CELL-1, CELL-1), 2)
        
        pygame.draw.rect(self.screen, (0, 255, 0), (*self.food, CELL, CELL)) # Food
        pygame.draw.rect(self.screen, (150, 0, 0), (*self.poison, CELL, CELL)) # Poison
        for o in self.obstacles: pygame.draw.rect(self.screen, (100, 100, 100), (*o, CELL, CELL))
        if self.powerup: pygame.draw.ellipse(self.screen, (255, 215, 0), (*self.powerup[0], CELL, CELL))

        self.draw_text(f"Score: {self.score}  Best: {self.best}  Lvl: {self.level}", 10, 10)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key == pygame.K_RETURN: 
                            self.p_id = self.db.get_player_id(self.username)
                            self.best = self.db.get_best(self.p_id); self.state = "PLAYING"
                        if event.key == pygame.K_l: self.state = "LEADERBOARD"
                        if event.key == pygame.K_s: self.state = "SETTINGS"
                    elif self.state == "PLAYING":
                        if event.key == pygame.K_UP and self.dir[1] == 0: self.dir = [0, -CELL]
                        elif event.key == pygame.K_DOWN and self.dir[1] == 0: self.dir = [0, CELL]
                        elif event.key == pygame.K_LEFT and self.dir[0] == 0: self.dir = [-CELL, 0]
                        elif event.key == pygame.K_RIGHT and self.dir[0] == 0: self.dir = [CELL, 0]
                    elif event.key == pygame.K_b: self.state = "MENU"
                    elif self.state == "GAMEOVER" and event.key == pygame.K_r: self.reset_game(); self.state = "MENU"

            if self.state == "PLAYING": self.update(); self.draw()
            elif self.state == "MENU":
                self.screen.fill((0,0,0))
                self.draw_text(f"Welcome, {self.username}", 330, 200)
                self.draw_text("ENTER - Play | L - Leaderboard | S - Settings", 220, 300)
                pygame.display.flip()
            elif self.state == "LEADERBOARD":
                self.screen.fill((0,0,0))
                self.draw_text("TOP 10 SCORES (Press B to Back)", 280, 50, (255, 215, 0))
                for i, row in enumerate(self.db.get_top_10()):
                    self.draw_text(f"{i+1}. {row[0]} - {row[1]} pts (Lvl {row[2]})", 280, 100 + i*30)
                pygame.display.flip()
            elif self.state == "SETTINGS":
                self.screen.fill((0,0,0))
                self.draw_text("SETTINGS (Press G to toggle Grid | C to change Color | B to Save)", 150, 250)
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_g: self.settings["grid"] = not self.settings["grid"]
                        if event.key == pygame.K_c: self.settings["snake_color"] = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
                        if event.key == pygame.K_b: save_settings(self.settings); self.state = "MENU"
                pygame.display.flip()
            elif self.state == "GAMEOVER":
                self.screen.fill((50,0,0))
                self.draw_text(f"GAME OVER! Score: {self.score}  Best: {self.best}", 250, 250)
                self.draw_text("Press R to return to Menu", 280, 300)
                pygame.display.flip()
            clock.tick(self.speed)

if __name__ == "__main__":
    SnakeGame().run()