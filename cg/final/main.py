import tkinter as tk

from player import *
from bullet import *
from asteroid import *
from explosion import *

class App:
    def __init__(self, root):
        self.__score = 0
        self.__lives = 3
        self.__root = root
        self.__root.title("Астероиды")
        self.__root.geometry("1000x600")

        self.__init_start_window()

    def __destroy_start_window(self):
        self.start_button.destroy()
        self.__game_frame.destroy()
    
    def __destroy_game_window(self):
        self.__canvas.destroy()
        self.__info_frame.destroy()

    def __init_start_window(self):
        self.__info_frame = tk.Frame(self.__root, width=200, height=800)
        self.__info_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.text_label = tk.Label(self.__info_frame, text="Some text here", wraplength=180)
        self.text_label.pack(pady=20)

        self.__game_frame = tk.Frame(self.__root, width=CANVAS_WIDTH, height=CANVAS_HEIGTH, background="yellow")
        self.__game_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.start_button = tk.Button(self.__game_frame, text="Start", command=self.__init_game_window)
        self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.lives_label = tk.Label(self.__game_frame, text="Lives: " + str(self.__lives))
        self.lives_label.place(x=10, y=10)

        self.score_label = tk.Label(self.__game_frame, text="Score: " + str(self.__score))
        self.score_label.place(x=CANVAS_WIDTH - 70, y=10)

    def __init_canvas_binds(self):
        self.__root.bind("<w>", lambda e: self.__player.set_moving_forward(True))
        self.__root.bind("<KeyRelease-w>", lambda e: self.__player.set_moving_forward(False))
        self.__root.bind("<a>", lambda e: setattr(self.__player, 'is_rotating_left', True))
        self.__root.bind("<KeyRelease-a>", lambda e: setattr(self.__player, 'is_rotating_left', False))
        self.__root.bind("<d>", lambda e: setattr(self.__player, 'is_rotating_right', True))
        self.__root.bind("<KeyRelease-d>", lambda e: setattr(self.__player, 'is_rotating_right', False))
        self.__root.bind("<space>", lambda e: setattr(self.__player, 'is_shooting', True))
        self.__root.bind("<KeyRelease-space>", lambda e: setattr(self.__player, 'is_shooting', False))

    def __init_start_options(self):
        self.__score = 0
        self.__lives = 3
        self.lives_id = self.__canvas.create_text(10, 10, text="Lives: " + str(self.__lives), anchor=tk.NW)
        self.score_id = self.__canvas.create_text(590, 10, text="Score: " + str(self.__score), anchor=tk.NE)

    def __init_game_window(self):
        self.__destroy_start_window()

        self.__canvas = tk.Canvas(self.__root, width=CANVAS_WIDTH, height=CANVAS_HEIGTH, bg="white")
        self.__canvas.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.__player = Player(self.__canvas)
        self.__asteroids = []
        self.__enable_check_collision = True
    
        self.__init_canvas_binds()
        self.__init_start_options()
        self.__generate_asteroid()
        self.__update_game()

    def __update_score(self):
        self.__score += 1
        self.__canvas.itemconfig(self.score_id, text="Score: " + str(self.__score))
        self.__init_canvas_binds()

    def __update_lives(self):
        self.__lives -= 1
        self.__canvas.itemconfig(self.lives_id, text="Score: " + str(self.__lives))

        self.__init_canvas_binds()

        if self.__lives == 0:
            self.__destroy_game_window()
            self.__asteroids = []
            self.__player.bullets = []
            self.__init_start_window()

    def __update_bullets(self):
        for bullet in self.__player.bullets[:]:
            if not bullet.move():
                self.__player.bullets.remove(bullet)
    
    def __update_asteroids(self):
        for asteroid in self.__asteroids:
            asteroid.move()

    def __generate_asteroid(self):
        self.__asteroids.append(Asteroid(self.__canvas, self.__player))
        self.__canvas.after(1000, self.__generate_asteroid)

    def __enable_collision_checking(self):
        self.__enable_check_collision = True

    def __is_collision(self, obj1, obj2):
        obj1_coords = self.__canvas.coords(obj1.id)
        obj2_coords = self.__canvas.coords(obj2.id)

        distance = ((obj1_coords[0] - obj2_coords[0]) ** 2 + (obj1_coords[1] - obj2_coords[1]) ** 2)

        if distance < ((obj1.size + obj2.size) / 2) ** 2:
            Explosion(self.__canvas, obj1_coords[0], obj1_coords[1])
            return True
        
        return False

    def __check_collision_bullet_asteroid(self):
        for bullet in self.__player.bullets[:]:
            for asteroid in self.__asteroids[:]:
                if self.__is_collision(bullet, asteroid):
                    self.__asteroids.remove(asteroid)
                    self.__player.bullets.remove(bullet)
                    self.__canvas.delete(bullet.id)
                    return True
        
        return False

    def __check_collision_player_asteroid(self):
        if not self.__enable_check_collision:
            return False

        self.__player.stop_blinking()

        for asteroid in self.__asteroids:
            if self.__is_collision(self.__player, asteroid):
                self.__player.start_blinking()
                self.__player.respawn()
                self.__enable_check_collision = False
                self.__canvas.after(5000, self.__enable_collision_checking)
                return True

        return False

    def __update_game(self):
        self.__update_bullets()
        self.__update_asteroids()

        if self.__check_collision_bullet_asteroid():
            self.__update_score()

        if self.__check_collision_player_asteroid():
            self.__player.respawn()
            self.__update_lives()

        self.__root.after(30, self.__update_game)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
