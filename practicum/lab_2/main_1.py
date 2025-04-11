import pygame
import random

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

def draw_house(screen):
    house_width = 200
    house_height = 150
    house_x = (SCREEN_WIDTH - house_width) // 2
    house_y = (SCREEN_HEIGHT - house_height) // 2 + 100

    pygame.draw.rect(screen, (139, 69, 19), (house_x, house_y, house_width, house_height))

    roof_points = [
        (house_x, house_y),
        (house_x + house_width // 2, house_y - 100),
        (house_x + house_width, house_y)
    ]

    pygame.draw.polygon(screen, (255, 0, 0), roof_points)

def draw_base_figures(screen):
    pygame.draw.circle(screen, 'red', [200, 100], 30)
    pygame.draw.circle(screen, [255, 152, 13], [100, 400], 50, width=15)
    pygame.draw.circle(screen, '#FFEE54', [400, 300], 100, width=5)

    pygame.draw.rect(screen, 'yellow', [400, 20, 300, 200], 0)

    for _ in range(5):
        top = random.randint(50, 700)
        left = random.randint(50, 500)
        w = random.randint(10, 200)
        h = random.randint(10, 100)
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        pygame.draw.rect(screen, color, [top, left, w, h], 4)

def draw_lines(screen):
    dots = [
        (221, 432), (225, 331), (133, 342), (141, 310),
        (51, 230), (47, 217), (58, 153), (114, 164),
        (123, 135), (176, 190), (159, 77), (193, 93),
        (230, 28), (267, 93), (301, 77), (284, 190),
        (327, 135), (336, 164), (402, 153), (386, 217),
        (409, 230), (319, 310), (327, 342), (233, 331),
        (237, 432),
    ]

    pygame.draw.lines(screen, 'green', True, dots, 2)

def draw_picuture(screen):
    apple = pygame.image.load('/home/denis/Downloads/apple.png')
    screen.blit(apple, (0, 100))
    pygame.display.flip()

    pygame.time.delay(2000)
    pygame.draw.rect(screen, 'white', (0, 100, 256, 256), 0)
    screen.blit(apple, (0, 300))

def base_settings():
    screen.fill([255, 255, 255])
    pygame.display.set_caption('Денис Кузнецов')

def main():
    global screen
    global pygame

    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    base_settings()
    draw_picuture(screen)
    draw_base_figures(screen)
    draw_lines(screen)
    draw_house(screen)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
