import random
from math import sin, cos, radians
from PIL import Image, ImageTk
from constants import *

class Asteroid:
    def __init__(self, canvas, player):
        self.canvas = canvas
        self.player_x, self.player_y = self.canvas.coords(player.id)
        self.size =  random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE) 
        self.angle = random.randint(ASTEROID_MIN_ANGLE, ASTEROID_MAX_ANGLE)
        self.speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        # self.x = self.generate_x_position(player_x)
        # self.y = self.generate_y_position(player_y)

        self.x = random.randint(ASTEROID_MIN_X, ASTEROID_MAX_X)
        self.y = random.randint(ASTEROID_MIN_Y, ASTEROID_MAX_Y)
        self.image_path = "./icons/meteor.png"
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((self.size, self.size), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def generate_x_position(self, player_x):
        x = random.randint(ASTEROID_MIN_X, ASTEROID_MAX_X)

        while abs(x - player_x) > DISTANCE_BEETWEN_PLAYER_ASTEROID:
            x = random.randint(ASTEROID_MIN_X, ASTEROID_MAX_X)

            if abs(x - player_x) < DISTANCE_BEETWEN_PLAYER_ASTEROID:
                return x

    
    def generate_y_position(self, player_y):
        y = random.randint(ASTEROID_MIN_Y, ASTEROID_MAX_Y)

        while abs(y - player_y) > DISTANCE_BEETWEN_PLAYER_ASTEROID:
            y = random.randint(ASTEROID_MIN_Y, ASTEROID_MAX_Y)

            if abs(y - player_y) < DISTANCE_BEETWEN_PLAYER_ASTEROID:
                return y

    def move(self):
        self.x += self.speed * sin(radians(self.angle))
        self.y -= self.speed * cos(radians(self.angle))

        if self.x < -self.size / 2:
            self.x = CANVAS_WIDTH + self.size / 2
        elif self.x > CANVAS_WIDTH + self.size / 2:
            self.x = -self.size / 2

        if self.y < -self.size / 2:
            self.y = CANVAS_HEIGTH + self.size / 2
        elif self.y > CANVAS_HEIGTH + self.size / 2:
            self.y = -self.size / 2

        self.canvas.coords(self.id, self.x, self.y)
