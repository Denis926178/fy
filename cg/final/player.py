from PIL import Image, ImageTk
from math import sin, cos, radians
from constants import *
from bullet import *

class Player:
    def __init__(self, canvas):
        # Settings of start position
        self.canvas = canvas
        self.size =       PLAYER_SIZE
        self.angle =      PLAYER_START_ANGLE
        self.x =          PLAYER_START_X
        self.y =          PLAYER_START_Y

        # Settings of speed player
        self.max_speed =  PLAYER_MAX_SPEED
        self.speed =      PLAYER_START_SPEED
        self.speed_up =   PLAYER_UP_SPEED
        self.speed_down = PLAYER_DOWN_SPEED

        # Flags for player's states
        self.is_moving_forward =      False
        self.is_rotating_left =       False
        self.is_rotating_right =      False
        self.is_shooting =            False
        self.shooting_allowed =       True
        self.blinking =               False

        self.position_changed = False
        self.angle_changed = False

        # Images for player
        self.image_path = "./icons/ship.png"
        self.image_boost_path = "./icons/ship_line.png"
    
        self.image = Image.open(self.image_path)
        self.image_boost = Image.open(self.image_boost_path)

        self.image = self.image.resize((self.size, self.size), Image.ANTIALIAS)
        self.image_boost = self.image_boost.resize((self.size, self.size), Image.ANTIALIAS)

        self.tk_image = ImageTk.PhotoImage(self.image)
        self.tk_image_boost = ImageTk.PhotoImage(self.image_boost)

        self.id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

        self.bullets = []
        self.update()

    def start_blinking(self):
        self.blinking = True
        self.blink()

    def blink(self):
        if self.blinking:
            if self.canvas.itemcget(self.id, "image") == str(self.tk_image):
                self.canvas.itemconfig(self.id, image="")
            else:
                self.canvas.itemconfig(self.id, image=self.tk_image)

            self.canvas.after(250, self.blink)

    def stop_blinking(self):
        self.blinking = False
        self.canvas.itemconfig(self.id, image=self.tk_image)

    def set_moving_forward(self, value):
        self.is_moving_forward = value

    def set_rotating_left(self, value):
        self.is_rotating_left = value

    def set_rotating_right(self, value):
        self.is_rotating_right = value

    def set_shooting(self, value):
        self.is_shooting = value

    def allow_shooting(self):
        self.shooting_allowed = True
 
    def respawn(self):
        self.x = 300
        self.y = 400
        self.angle = 0
        self.draw()

    def draw(self):
        rotated_image = self.image.rotate(-self.angle, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.id, image=self.tk_image)
        self.canvas.coords(self.id, self.x, self.y)
    
    # def draw(self):
    #     rotated_image = self.image_boost.rotate(-self.angle, expand=True)
    #     self.tk_image_boost = ImageTk.PhotoImage(rotated_image)
    #     self.canvas.itemconfig(self.id, image=self.tk_image_boost)
    #     self.canvas.coords(self.id, self.x, self.y)

    def move_forward(self):
        self.x += self.speed * sin(radians(self.angle))
        self.y -= self.speed * cos(radians(self.angle))

        if self.x < -self.size / 2:
            self.x = 600 + self.size / 4
        elif self.x > 675 + self.size / 2:
            self.x = 0

        if self.y < -self.size / 2:
            self.y = 800 + self.size / 4
        elif self.y > 800 + self.size / 2:
            self.y = 0

    def turn_left(self):
        self.angle -= 10

    def turn_right(self):
        self.angle += 10

    def update(self):
        if self.is_moving_forward:
            self.speed = min(self.max_speed, self.speed + self.speed_up)
        else:
            self.speed = max(0, self.speed - self.speed_down)

        self.move_forward()

        if self.is_rotating_left:
            self.turn_left()
        if self.is_rotating_right:
            self.turn_right()
        if self.is_shooting:
            self.shoot()

        self.draw()
        self.canvas.after(50, self.update)

    def shoot(self):
        if self.shooting_allowed:
            bullet_x = self.x + (self.size / 2) * sin(radians(self.angle))
            bullet_y = self.y - (self.size / 2) * cos(radians(self.angle))
            bullet = Bullet(self.canvas, bullet_x, bullet_y, self.angle)
            self.bullets.append(bullet)
            self.shooting_allowed = False
            self.canvas.after(200, self.allow_shooting)
