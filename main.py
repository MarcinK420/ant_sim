import pygame
import random
import math
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
ant_speed = 0.05
ant_angle = random.uniform(0, 2 * math.pi)

last_move_time = 0
move_interval = 1000

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, ant_color, (int(ant_x), int(ant_y)), ant_size)
    pygame.display.flip()

    ant_x += ant_speed * math.cos(ant_angle)
    ant_y += ant_speed * math.sin(ant_angle)
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > move_interval:
        ant_angle = random.uniform(0, 2 * math.pi)
        last_move_time = current_time

    if ant_x < 0 or ant_x > SCREEN_WIDTH:
        ant_angle = math.pi - ant_angle
    if ant_y < 0 or ant_y > SCREEN_HEIGHT:
        ant_angle = -ant_angle

pygame.quit()
