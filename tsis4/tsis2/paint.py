import pygame
import datetime
from collections import deque

# Инициализация
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application - TSIS 2")

# Цвета
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Холст (отдельный слой для рисования)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Состояние приложения
running = True
drawing = False
mode = 'pencil' 
current_color = BLACK
brush_size = 5
start_pos = None
text_content = ""
text_pos = None

# Вывод инструкций в консоль
print("--- ИНСТРУКЦИЯ (TSIS 2) ---")
print("P - Кисть (Pencil)")
print("L - Прямая линия (Line)")
print("R - Прямоугольник (Rectangle)")
print("C - Круг (Circle)")
print("F - Заливка (Flood Fill)")
print("T - Текст (Кликните на холст, печатайте, Enter - подтвердить, Esc - отмена)")
print("E - Ластик (Eraser)")
print("1, 2, 3 - Изменение размера кисти")
print("Ctrl + S - Сохранить холст (.png)")
print("--------------------------")

def flood_fill(surface, x, y, new_color):
    """Алгоритм заливки (BFS)"""
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    queue = deque([(x, y)])
    while queue:
        curr_x, curr_y = queue.popleft()
        if not (0 <= curr_x < WIDTH and 0 <= curr_y < HEIGHT): continue
        if surface.get_at((curr_x, curr_y)) != target_color: continue
        surface.set_at((curr_x, curr_y), new_color)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            queue.append((curr_x + dx, curr_y + dy))

while running:
    # Отрисовка интерфейса и холста
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    # Живой предпросмотр фигур при перетаскивании
    if drawing and start_pos:
        curr_pos = pygame.mouse.get_pos()
        if mode == 'line':
            pygame.draw.line(screen, current_color, start_pos, curr_pos, brush_size)
        elif mode == 'rect':
            r = pygame.Rect(min(start_pos[0], curr_pos[0]), min(start_pos[1], curr_pos[1]), 
                            abs(start_pos[0]-curr_pos[0]), abs(start_pos[1]-curr_pos[1]))
            pygame.draw.rect(screen, current_color, r, brush_size)
        elif mode == 'circle':
            radius = int(((start_pos[0]-curr_pos[0])**2 + (start_pos[1]-curr_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ПРОВЕРКА: Если мы в режиме ввода текста, блокируем хоткеи
            if mode == 'text' and text_pos is not None:
                if event.key == pygame.K_RETURN:
                    f = pygame.font.SysFont("Arial", 24)
                    canvas.blit(f.render(text_content, True, current_color), text_pos)
                    text_content = ""; text_pos = None
                    print("Текст зафиксирован.")
                elif event.key == pygame.K_ESCAPE:
                    text_content = ""; text_pos = None
                    print("Ввод текста отменен.")
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode
                continue # Пропускаем остальную логику KEYDOWN

            # ОБЫЧНЫЕ ХОТКЕИ (срабатывают, только если не печатаем текст)
            key_name = pygame.key.name(event.key).lower()
            
            if key_name == 'p': 
                mode = 'pencil'; current_color = BLACK; print("Инструмент: Кисть")
            elif key_name == 'l': 
                mode = 'line'; current_color = BLACK; print("Инструмент: Линия")
            elif key_name == 'r': 
                mode = 'rect'; current_color = BLACK; print("Инструмент: Прямоугольник")
            elif key_name == 'c': 
                mode = 'circle'; current_color = BLACK; print("Инструмент: Круг")
            elif key_name == 'f': 
                mode = 'fill'; print("Инструмент: Заливка")
            elif key_name == 't': 
                mode = 'text'; print("Инструмент: Текст (кликните на холст)")
            elif key_name == 'e': 
                mode = 'pencil'; current_color = WHITE; print("Инструмент: Ластик")
            
            # Настройка размера (клавиши 1, 2, 3)
            if event.key == pygame.K_1: brush_size = 2; print("Размер: 2")
            elif event.key == pygame.K_2: brush_size = 5; print("Размер: 5")
            elif event.key == pygame.K_3: brush_size = 10; print("Размер: 10")
            
            # Сохранение Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                pygame.image.save(canvas, f"paint_{ts}.png")
                print(f"Холст сохранен как paint_{ts}.png")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'fill':
                flood_fill(canvas, event.pos[0], event.pos[1], current_color)
            elif mode == 'text':
                text_pos = event.pos
                text_content = ""
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end_pos = event.pos
                if mode == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)
                elif mode == 'rect':
                    r = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), 
                                    abs(start_pos[0]-end_pos[0]), abs(start_pos[1]-end_pos[1]))
                    pygame.draw.rect(canvas, current_color, r, brush_size)
                elif mode == 'circle':
                    radius = int(((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                drawing = False
                start_pos = None

        if event.type == pygame.MOUSEMOTION and drawing and mode == 'pencil':
            # Свободное рисование
            pygame.draw.circle(canvas, current_color, event.pos, brush_size)

    # Отображение вводимого текста в реальном времени
    if mode == 'text' and text_pos:
        f = pygame.font.SysFont("Arial", 24)
        screen.blit(f.render(text_content + "|", True, BLACK), text_pos)

    pygame.display.flip()

pygame.quit()