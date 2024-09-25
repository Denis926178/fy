import tkinter as tk
import random

from constants import *

class Bullets:
    def __init__(self, canvas):
        self.__bullets = []
        self.__canvas = canvas
    
    def create(self, player):
        x1, y1, x2, y2 = self.__canvas.coords(player)
        bullet = self.__canvas.create_rectangle(x1 + (PLAYER_WIDTH - BULLET_WIDTH) // 2, 
                                                y1 - BULLET_HEIGHT, 
                                                x1 + (PLAYER_WIDTH + BULLET_WIDTH) // 2, 
                                                y1, fill=BULLET_COLOR)
        self.__bullets.append(bullet)
        
    def move(self):
        for bullet in self.__bullets:
            self.__canvas.move(bullet, 0, -10)
            if self.__canvas.coords(bullet)[1] < CANVAS_PADDING:
                self.delete_bullet(bullet)

    def check_collision(self, asteroid):
        ax1, ay1, ax2, ay2 = self.__canvas.coords(asteroid)

        for bullet in self.__bullets:
            bx1, by1, bx2, by2 = self.__canvas.coords(bullet)
            if ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1:
                self.delete_bullet(bullet)
                return True

        return False

    def delete_bullet(self, bullet):
        self.__canvas.delete(bullet)
        self.__bullets.remove(bullet)

class Game:
    def __init__(self):
        self.__root = tk.Tk()
        self.__canvas = tk.Canvas(self.__root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_COLOR)
        self.__canvas.pack()
        self.__start()

    def __start(self):
        self.__player = self.__canvas.create_rectangle((CANVAS_WIDTH - PLAYER_WIDTH) // 2, 
                                                        CANVAS_HEIGHT - PLAYER_HEIGHT - CANVAS_PADDING, 
                                                        (CANVAS_WIDTH + PLAYER_WIDTH ) // 2, 
                                                        CANVAS_HEIGHT - CANVAS_PADDING, 
                                                        fill=PLAYER_COLOR)
        self.__bullets = Bullets(self.__canvas)
        self.__asteroids = []
        self.__score = 0
        self.__can_shoot = True

        self.__score_text = self.__canvas.create_text(550, 20, text=f"Score: {self.__score}", fill="white", font=("Arial", 16))

        self.__root.bind("<Left>", self.__move_left)
        self.__root.bind("<Right>", self.__move_right)
        self.__root.bind("<space>", self.__shoot)
        
        self.__spawn_asteroid()
        self.__update()

    def __move_left(self, event):
        if self.__canvas.coords(self.__player)[0] > CANVAS_PADDING:
            self.__canvas.move(self.__player, -20, 0)

    def __move_right(self, event):
        if self.__canvas.coords(self.__player)[2] < CANVAS_WIDTH - CANVAS_PADDING:
            self.__canvas.move(self.__player, 20, 0)

    def __shoot(self, event):
        if not self.__can_shoot:
            return

        self.__bullets.create(self.__player)
        self.__can_shoot = False
        self.__root.after(TIMEOUT_SHOOT_MC, self.__allow_shooting)

    def __allow_shooting(self):
        self.__can_shoot = True

    def __spawn_asteroid(self):
        width = random.randint(MIN_WIDTH_ASTEROID, MAX_WIDTH_ASTEROID)
        height = random.randint(MIN_HEIGHT_ASTEROID, MAX_HEIGHT_ASTEROID)
        x = random.randint(0, CANVAS_WIDTH - CANVAS_PADDING - width)
        speed = random.uniform(MIN_SPEED_ASTEROID, MAX_SPEED_ASTEROID)
        angle = random.uniform(-1, 1)
        asteroid = self.__canvas.create_rectangle(x, 0, x + width, height, fill="red")
        self.__asteroids.append((asteroid, speed, angle))
        self.__root.after(TIMEOUT_ASTEROID_MC, self.__spawn_asteroid)
    
    def __delete_asteroid(self, asteroid):
        self.__canvas.delete(asteroid[0])
        self.__asteroids.remove(asteroid)

    def __update(self):
        self.__bullets.move()

        for asteroid, speed, angle in self.__asteroids:
            self.__canvas.move(asteroid, angle * speed, speed)
            if self.__canvas.coords(asteroid)[3] > CANVAS_WIDTH - CANVAS_PADDING:
                self.__delete_asteroid((asteroid, speed, angle))
            elif self.__check_collision_with_bullet(asteroid):
                self.__score += 1
                self.__canvas.itemconfig(self.__score_text, text=f"Score: {self.__score}")
                self.__delete_asteroid((asteroid, speed, angle))
            elif self.__check_collision_with_player(asteroid):
                self.__canvas.create_text(300, 300, text="GAME OVER", fill="white", font=("Arial", 24))
                self.__create_restart_button()
                return

        self.__root.after(50, self.__update)

    def __check_collision_with_bullet(self, asteroid):
        return self.__bullets.check_collision(asteroid)

    def __check_collision_with_player(self, asteroid):
        ax1, ay1, ax2, ay2 = self.__canvas.coords(asteroid)
        px1, py1, px2, py2 = self.__canvas.coords(self.__player)

        return ax1 < px2 and ax2 > px1 and ay1 < py2 and ay2 > py1

    def __create_restart_button(self):
        self.__restart_button = tk.Button(self.__root, text="Restart", command=self.__restart_game)
        self.__restart_button.pack()

    def __restart_game(self):
        self.__canvas.delete("all")
        self.__restart_button.destroy()
        self.__restart_button = None
        self.__start()

    def run(self):
        self.__root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()
