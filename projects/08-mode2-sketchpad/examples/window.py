import pygame

pygame.init()
window = pygame.display.set_mode((640, 512))
pygame.display.set_caption("Hello, Pygame")
clock = pygame.time.Clock()

x = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x = (x + 4) % 640

    window.fill("black")
    pygame.draw.circle(window, "yellow", (x, 256), 40)
    pygame.display.flip()

    clock.tick(50)

pygame.quit()
