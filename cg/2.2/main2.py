import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Анимация фигур')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Shape:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def draw(self):
        pass

    def move(self):
        self.x += self.speed
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.speed = -self.speed
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def is_clicked(self, mouse_pos):
        pass

class Rectangle(Shape):
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

class Circle(Shape):
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)

    def is_clicked(self, mouse_pos):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return (mouse_pos[0] - center_x) ** 2 + (mouse_pos[1] - center_y) ** 2 <= (self.width // 2) ** 2

class Triangle(Shape):
    def draw(self):
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)

    def is_clicked(self, mouse_pos):
        x1, y1 = self.x + self.width // 2, self.y
        x2, y2 = self.x, self.y + self.height
        x3, y3 = self.x + self.width, self.y + self.height

        def cross_product(a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

        d1 = cross_product((x1, y1), (x2, y2), mouse_pos)
        d2 = cross_product((x2, y2), (x3, y3), mouse_pos)
        d3 = cross_product((x3, y3), (x1, y1), mouse_pos)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

shapes = [
    Rectangle(100, 200, 50, 50, (255, 0, 0), 5),
    Rectangle(200, 300, 80, 40, (0, 255, 0), 3),
    Circle(400, 100, 60, 60, (0, 0, 255), 4),
    Triangle(500, 400, 70, 70, (255, 255, 0), 2)
]

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for shape in shapes:
                if shape.is_clicked(mouse_pos):
                    shape.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    for shape in shapes:
        shape.move()
        shape.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
