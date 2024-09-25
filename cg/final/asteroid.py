import random
from math import sin, cos, radians
from PIL import Image, ImageTk
from constants import *

class Asteroid:
    __image_cache = None

    def __init__(self, canvas, player):
        self.canvas = canvas
        self.player_x, self.player_y = self.canvas.coords(player.id)
        self.size = random.randrange(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE + 1, 10)
        self.angle = random.randint(ASTEROID_MIN_ANGLE, ASTEROID_MAX_ANGLE)
        self.speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.x = self.generate_x_position()
        self.y = self.generate_y_position()
    
        if Asteroid.__image_cache is None:
            image_path = "./icons/meteor.png"
            image = Image.open(image_path)
            Asteroid.__image_cache = image

        self.image = Asteroid.__image_cache.resize((self.size, self.size), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def generate_x_position(self):
        while True:
            x = random.randint(ASTEROID_MIN_X, ASTEROID_MAX_X)
            if abs(x - self.player_x) > DISTANCE_BEETWEN_PLAYER_ASTEROID:
                return x

    def generate_y_position(self):
        while True:
            y = random.randint(ASTEROID_MIN_Y, ASTEROID_MAX_Y)
            if abs(y - self.player_y) > DISTANCE_BEETWEN_PLAYER_ASTEROID:
                return y

    def move(self):
        self.x = (self.x + self.speed * sin(radians(self.angle))) % (CANVAS_WIDTH + self.size)
        self.y = (self.y - self.speed * cos(radians(self.angle))) % (CANVAS_HEIGTH + self.size)

        self.canvas.coords(self.id, self.x, self.y)
