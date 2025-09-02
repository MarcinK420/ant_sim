import pygame
import random
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Symulator Mrowiska")

ant_x = SCREEN_WIDTH // 2
ant_y = SCREEN_HEIGHT // 2
ant_color = (255, 0, 0)
ant_size = 5
# Prędkość mrówki
ant_dx = 0.05
ant_dy = 0.05

last_move_time = 0
move_interval = 1000

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, ant_color, (ant_x, ant_y), ant_size)
    pygame.display.flip()

    ant_x += ant_dx
    ant_y += ant_dy
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > move_interval:
        ant_dx = random.choice([-ant_dx, ant_dx])
        ant_dy = random.choice([-ant_dy, ant_dy])
        last_move_time = current_time

    if ant_x < 0 or ant_x > SCREEN_WIDTH:
        ant_dx = -ant_dx
    if ant_y < 0 or ant_y > SCREEN_HEIGHT:
        ant_dy = -ant_dy

pygame.quit()
