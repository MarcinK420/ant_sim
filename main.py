import pygame
import random
import math
import numpy as np

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Symulator Mrowiska")

# Parametry mrówki
ant_x = SCREEN_WIDTH // 2
ant_y = SCREEN_HEIGHT // 2
ant_color = (255, 0, 0)  # czerwony
ant_size = 5
ant_speed = 0.5
ant_angle = random.uniform(0, 2 * math.pi)

# Timer losowej zmiany kierunku
last_move_time = 0
move_interval = 1000

# Jedzenie
food_positions = []
food_color = (0, 255, 0)  # zielony
food_size = 3
food_count = 15

# Generujemy losowe pozycje jedzenia
for _ in range(food_count):
    food_x = random.randint(food_size, SCREEN_WIDTH - food_size)
    food_y = random.randint(food_size, SCREEN_HEIGHT - food_size)
    food_positions.append((food_x, food_y))

# === NOWE: System feromonów ===
pheromone_grid_size = 10  # jeden "piksel" feromonu = 10x10 pikseli ekranu
pheromone_width = SCREEN_WIDTH // pheromone_grid_size
pheromone_height = SCREEN_HEIGHT // pheromone_grid_size
pheromone_map = np.zeros((pheromone_height, pheromone_width))

pheromone_strength = 100.0  # siła feromonu zostawianego przy jedzeniu
pheromone_decay = 0.99      # współczynnik parowania (0.99 = 1% na klatkę)
pheromone_influence = 0.3   # jak mocno feromony wpływają na ruch (0-1)

def add_pheromone(x, y, strength):
    """Dodaje feromon w danej pozycji"""
    grid_x = int(x // pheromone_grid_size)
    grid_y = int(y // pheromone_grid_size)
    if 0 <= grid_x < pheromone_width and 0 <= grid_y < pheromone_height:
        pheromone_map[grid_y, grid_x] += strength

def get_pheromone_gradient(x, y):
    """Zwraca kierunek najsilniejszego feromonu w okolicy"""
    grid_x = int(x // pheromone_grid_size)
    grid_y = int(y // pheromone_grid_size)
    
    # Sprawdzamy 8 sąsiadów + centrum
    max_pheromone = 0
    best_direction = None
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
                
            nx, ny = grid_x + dx, grid_y + dy
            if 0 <= nx < pheromone_width and 0 <= ny < pheromone_height:
                pheromone_level = pheromone_map[ny, nx]
                if pheromone_level > max_pheromone:
                    max_pheromone = pheromone_level
                    # Obliczamy kąt do tego miejsca
                    target_x = (nx + 0.5) * pheromone_grid_size
                    target_y = (ny + 0.5) * pheromone_grid_size
                    best_direction = math.atan2(target_y - y, target_x - x)
    
    return best_direction, max_pheromone

def draw_pheromones():
    """Rysuje feromony jako półprzezroczyste niebieskie prostokąty"""
    max_pheromone = np.max(pheromone_map) if np.max(pheromone_map) > 0 else 1
    
    for y in range(pheromone_height):
        for x in range(pheromone_width):
            pheromone_level = pheromone_map[y, x]
            if pheromone_level > 1:  # Rysuj tylko widoczne feromony
                alpha = min(255, int(255 * pheromone_level / max_pheromone * 0.5))
                color = (0, 0, 255, alpha)  # niebieski z alpha
                
                rect = pygame.Rect(
                    x * pheromone_grid_size,
                    y * pheromone_grid_size,
                    pheromone_grid_size,
                    pheromone_grid_size
                )
                
                # Tworzymy surface z alpha dla przezroczystości
                pheromone_surface = pygame.Surface((pheromone_grid_size, pheromone_grid_size))
                pheromone_surface.set_alpha(alpha)
                pheromone_surface.fill((0, 100, 255))  # jasnoniebieski
                screen.blit(pheromone_surface, rect)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Czyszczenie ekranu
    screen.fill((0, 0, 0))
    
    # Rysowanie feromonów (pod wszystkimi obiektami)
    draw_pheromones()
    
    # Rysowanie jedzenia
    for food_pos in food_positions:
        pygame.draw.circle(screen, food_color, food_pos, food_size)
    
    # Rysowanie mrówki
    pygame.draw.circle(screen, ant_color, (int(ant_x), int(ant_y)), ant_size)
    
    # Wykrywanie kolizji mrówki z jedzeniem
    for i, food_pos in enumerate(food_positions):
        distance = math.sqrt((ant_x - food_pos[0])**2 + (ant_y - food_pos[1])**2)
        if distance < ant_size + food_size:
            # Mrówka zjadła jedzenie!
            food_positions.pop(i)
            
            # === NOWE: Zostawiamy feromon! ===
            add_pheromone(ant_x, ant_y, pheromone_strength)
            print(f"Mrówka zjadła jedzenie i zostawiła feromon! Pozostało: {len(food_positions)}")
            break

    # === NOWE: Wpływ feromonów na ruch ===
    pheromone_direction, pheromone_level = get_pheromone_gradient(ant_x, ant_y)
    
    # Losowa zmiana kierunku (teraz rzadziej gdy są feromony)
    current_time = pygame.time.get_ticks()
    should_change_direction = current_time - last_move_time > move_interval
    
    # Jeśli są feromony, mieszamy losowy ruch z podążaniem za feromonami
    if should_change_direction:
        if pheromone_direction is not None and pheromone_level > 5:
            # Mieszamy losowy kierunek z kierunkiem feromonu
            random_angle = random.uniform(0, 2 * math.pi)
            ant_angle = (1 - pheromone_influence) * random_angle + pheromone_influence * pheromone_direction
        else:
            # Brak feromonów - losowy ruch jak wcześniej
            ant_angle = random.uniform(0, 2 * math.pi)
        
        last_move_time = current_time

    # Ruch mrówki
    ant_x += ant_speed * math.cos(ant_angle)
    ant_y += ant_speed * math.sin(ant_angle)

    # Odbicia od ścian
    if ant_x < 0 or ant_x > SCREEN_WIDTH:
        ant_angle = math.pi - ant_angle
    if ant_y < 0 or ant_y > SCREEN_HEIGHT:
        ant_angle = -ant_angle

    # === NOWE: Parowanie feromonów ===
    pheromone_map *= pheromone_decay
    
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()