import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import random

class BarnsleyFern:
    def __init__(self, canvas):
        self.canvas = canvas
        self.iterations = 100000
        self.x = [0]
        self.y = [0]

    def draw(self):
        for _ in range(self.iterations):
            x_last = self.x[-1]
            y_last = self.y[-1]
            rand = random.random()

            if rand <= 0.01:
                x_new = 0
                y_new = 0.16 * y_last
            elif rand <= 0.86:
                x_new = 0.85 * x_last + 0.04 * y_last
                y_new = -0.04 * x_last + 0.85 * y_last + 1.6
            elif rand <= 0.93:
                x_new = 0.2 * x_last - 0.26 * y_last
                y_new = 0.23 * x_last + 0.22 * y_last + 1.6
            else:
                x_new = -0.15 * x_last + 0.28 * y_last
                y_new = 0.26 * x_last + 0.24 * y_last + 0.44

            self.x.append(x_new)
            self.y.append(y_new)

            canvas_x = int(300 + x_new * 50)
            canvas_y = int(550 - y_new * 50)

            self.canvas.create_line(canvas_x, canvas_y, canvas_x + 1, canvas_y + 1, fill="black")

class KochSnowflake:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, x1 = 300, y1 = 50, x2 = 100, y2 = 500, x3 = 500, y3 = 500, order = 3):
        self.draw_segment(x1, y1, x2, y2, order)
        self.draw_segment(x2, y2, x3, y3, order)
        self.draw_segment(x3, y3, x1, y1, order)

    def draw_segment(self, x1, y1, x2, y2, order):
        if order == 0:
            self.canvas.create_line(x1, y1, x2, y2, fill="blue")
        else:
            dx = x2 - x1
            dy = y2 - y1
            
            xA = x1 + dx / 3
            yA = y1 + dy / 3
            
            xB = x1 + dx / 2 - dy * (3 ** 0.5) / 6
            yB = y1 + dy / 2 + dx * (3 ** 0.5) / 6
            
            xC = x1 + 2 * dx / 3
            yC = y1 + 2 * dy / 3

            self.draw_segment(x1, y1, xA, yA, order - 1)
            self.draw_segment(xA, yA, xB, yB, order - 1)
            self.draw_segment(xB, yB, xC, yC, order - 1)
            self.draw_segment(xC, yC, x2, y2, order - 1)

class SierpinskiTriangle:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_triangle(self, x1, y1, x2, y2, x3, y3):
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", fill="black")

    def draw(self, x1 = 300, y1 = 50, x2 = 100, y2 = 550, x3 = 500, y3 = 550, order = 8):
        if order == 0:
            self.draw_triangle(x1, y1, x2, y2, x3, y3)
        else:
            x12 = (x1 + x2) / 2
            y12 = (y1 + y2) / 2
            x23 = (x2 + x3) / 2
            y23 = (y2 + y3) / 2
            x31 = (x3 + x1) / 2
            y31 = (y3 + y1) / 2

            self.draw(x1, y1, x12, y12, x31, y31, order - 1)
            self.draw(x2, y2, x12, y12, x23, y23, order - 1)
            self.draw(x3, y3, x31, y31, x23, y23, order - 1)

class Application:
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __init_main(self):
        self.__root = tk.Tk()
        self.__root.title("Фрактал")

    def __init_canvas(self):
        self.__canvas = tk.Canvas(self.__root, width=600,
                                               height=700, 
                                               bg="white")
    
        self.__canvas.grid(row=0, column=0, columnspan=2)

    def __init_BarnsleyFern(self):
        self.__BarnsleyFern_btn = ttk.Radiobutton(text="Папоротник Барнсли", value="Папоротник Барнсли", command=self.__draw_fern)
        self.__BarnsleyFern_btn.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    def __init_SierpinskiTriangle(self):
        self.__SierpinskiTriangle_btn = ttk.Radiobutton(text="Треугольник Серпинского", value="Треугольник Серпинского", command=self.__draw_triangle)
        self.__SierpinskiTriangle_btn.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    def __init_KochSnowflake(self):
        self.__KochSnowflake_btn = ttk.Radiobutton(text="Снежинка Коха", value="Снежинка Коха", command=self.__draw_snowflake)
        self.__KochSnowflake_btn.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    def __init_button_draw(self):
        self.__draw_btn = ttk.Button(text="Построить", command=self.__draw)
        self.__draw_btn.grid(row=1, column=1, rowspan=3)
    
    def __draw_fern(self):
        self.__figure = BarnsleyFern(self.__canvas)

    def __draw_triangle(self):
        self.__figure = SierpinskiTriangle(self.__canvas)
    
    def __draw_snowflake(self):
        self.__figure = KochSnowflake(self.__canvas)

    def __draw(self):
        self.__canvas.delete("all")
        self.__figure.draw()

    def __initUI(self):
        self.__init_main()
        self.__init_canvas()
        self.__init_BarnsleyFern()
        self.__init_SierpinskiTriangle()
        self.__init_KochSnowflake()
        self.__init_button_draw()

    def run(self):
        self.__root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
