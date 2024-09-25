from math import sin, cos, radians
from PIL import Image, ImageTk, ImageDraw
from constants import *

class Bullet:
    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.start_x = x
        self.start_y = y
        self.x =       x
        self.y =       y
        self.angle =   angle

        self.speed =        BULLET_SPEED
        self.size =         BULLET_SIZE
        self.max_distance = BULLET_MAX_DISTANCE
        
        self.image = self.create_gradient_orange_circle()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def create_gradient_orange_circle(self):
        image = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        for i in range(self.size // 2, 0, -1):
            color = (255, 165, 0, int(255 * (i / (self.size // 2))))
            draw.ellipse((self.size // 2 - i, self.size // 2 - i, self.size // 2 + i, self.size // 2 + i), fill=color)

        return image

    def move(self):
        self.x += self.speed * sin(radians(self.angle))
        self.y -= self.speed * cos(radians(self.angle))
        self.canvas.coords(self.id, self.x, self.y)

        distance = ((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2) ** 0.5
        
        if (self.x < 0 or self.x > self.canvas.winfo_width() or
                self.y < 0 or self.y > self.canvas.winfo_height() or distance > self.max_distance):
            self.canvas.delete(self.id)
            return False

        return True
