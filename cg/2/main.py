import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class GraphPolar:
    def __init__(self, n, d):
        self.__theta = np.linspace(0, 20 * np.pi, 10000)
        self.__graph = np.sin(round(n, 1) / round(d, 1) * self.__theta)
    
    def draw(self, canvas, ax):
        ax.clear()

        ax.plot(self.__theta, self.__graph)
        ax.set_aspect('equal')
        ax.set_facecolor('black')
        ax.grid(True, color='gray')

        canvas.draw()
    
class Application:
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __init_main(self):
        self.__root = tk.Tk()
        self.__root.title("Полярная роза")

    def __init_canvas(self):
        self.__canvas = FigureCanvasTkAgg(self.__fig, master=self.__root)
        self.__canvas..grid(row=0, column=0, columnspan=2)

    def __init_n_param(self):
        self.__n = tk.DoubleVar(value = 5)
        self.__slider_n = ttk.Scale(self.__root, from_=1, to_=10, orient='horizontal', variable=self.__n, command=self.__draw_plot)
        self.__slider_n.set(5)
        self.__slider_n.grid(row=1, column=0, padx=10, pady=10)
        ttk.Label(self.__root, text="Параметр n").grid(row=2, column=0)
    
    def __init_d_param(self):
        self.__d = tk.DoubleVar(value = 1)
        self.__slider_d = ttk.Scale(self.__root, from_=1, to_=20, orient='horizontal', variable= self.__d, command=self.__draw_plot)
        self.__slider_d.set(1)
        self.__slider_d.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self.__root, text="Параметр d").grid(row=2, column=1)

    def __draw_plot(self, value = 0):
        self.__graph = GraphPolar(self.__n.get(), self.__d.get())
        self.__graph.draw(self.__canvas, self.__ax)

    def __initUI(self):
        self.__init_main()
        self.__init_canvas()
        self.__init_n_param()
        self.__init_d_param()
        self.__draw_plot()
    
    def run(self):
        self.__root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
