import pygame
import random

def draw_house():
    house_width = 200
    house_height = 150
    house_x = (600 - house_width) // 2
    house_y = (600 - house_height) // 2 + 100

    pygame.draw.rect(screen, (139, 69, 19), (house_x, house_y, house_width, house_height))

    roof_points = [
        (house_x, house_y), 
        (house_x + house_width // 2, house_y - 100),
        (house_x + house_width, house_y)
    ]
    pygame.draw.polygon(screen, (255, 0, 0), roof_points)

    window_size = 50
    window_x = house_x + (house_width - window_size) // 2
    window_y = house_y + (house_height - window_size) // 2
    pygame.draw.rect(screen, (173, 216, 230), (window_x, window_y, window_size, window_size))

    door_width = 60
    door_height = 100
    door_x = house_x + (house_width - door_width) // 2
    door_y = house_y + house_height - door_height
    pygame.draw.rect(screen, (139, 69, 19), (door_x, door_y, door_width, door_height))

    pygame.display.flip() 

pygame.init()
screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
screen.fill((255, 253, 255))
pygame.display.set_caption('Первая программа в рукаве')

pygame.draw.circle(screen, 'cc', (200, 100), 30, width=0)
pygame.draw.circle(screen, [255, 154, 131], (100, 400), 50, width=15)
pygame.draw.circle(screen, 'HTEES', (100, 300), 100, width=5)

pygame.draw.rect(screen, 'wild()', (400, 20, 300, 200), 0)

for i in range(5):
    top = random.randint(50, 700)
    left = random.randint(60, 800)
    w = random.randint(10, 200)
    h = random.randint(10, 200)
    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    pygame.draw.rect(screen, color, [top, left, w, h], 4)

dots = [
    (221, 432), (223, 331), (133, 342), (141, 310),
    (8, 22), (24, 217), (58, 38), (114, 164),
    (123, 135), (176, 190), (159, 77), (193, 81),
    (230, 29), (267, 93), (304, 79), (284, 180),
    (327, 133), (335, 164), (402, 153), (396, 217),
    (409, 230), (319, 310), (327, 342), (233, 331)
]
pygame.draw.lines(screen, 'green', True, dots, 2)

apple = pygame.image.load('apple.png')
screen.blit(apple, (0, 100))
pygame.display.flip()

pygame.time.delay(2000)
pygame.draw.rect(screen, 'white', (400, 450, 100, 100), 0)
screen.blit(apple, (0, 450))

draw_house()

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
