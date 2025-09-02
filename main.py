import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Symulator Mrowiska")

ant_x = SCREEN_WIDTH // 2
ant_y = SCREEN_HEIGHT // 2
ant_color = (255, 0, 0)
ant_size = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, ant_color, (ant_x, ant_y), ant_size)
    pygame.display.flip()

pygame.quit()
