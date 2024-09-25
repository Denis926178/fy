from math import sin, cos, radians
from PIL import Image, ImageTk, ImageDraw
from constants import *

class Bullet:
    speed =        BULLET_SPEED
    size =         BULLET_SIZE
    max_distance = BULLET_MAX_DISTANCE

    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.start_x = x
        self.start_y = y
        self.x =       x
        self.y =       y
        self.angle =   angle
        
        if not hasattr(Bullet, 'tk_image'):
            Bullet.image = self.create_gradient_orange_circle()
            Bullet.tk_image = ImageTk.PhotoImage(self.image)

        self.id = self.canvas.create_image(self.x, self.y, image=Bullet.tk_image)

    @classmethod
    def create_gradient_orange_circle(cls):
        image = Image.new('RGBA', (cls.size, cls.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        for i in range(cls.size // 2, 0, -1):
            color = (255, 165, 0, int(255 * (i / (cls.size // 2))))
            draw.ellipse((cls.size // 2 - i, cls.size // 2 - i,
                           cls.size // 2 + i, cls.size // 2 + i), fill=color)

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
