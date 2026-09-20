import pygame

pygame.init()
window = pygame.display.set_mode((640, 512))
pygame.display.set_caption("Moiré")
clock = pygame.time.Clock()

window.fill("black")
for x in range(0, 640, 8):
    pygame.draw.line(window, "red", (0, 511), (x, 0))
    pygame.draw.line(window, "yellow", (639, 511), (639 - x, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
