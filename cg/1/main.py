import tkinter as tk
import math

from constants import *

class Circle:
    def __init__(self):
        self.__radius = CIRCLE_RADIUS
        self.__center_x = CIRCLE_CENTER_X
        self.__center_y = CIRCLE_CONTER_Y

    def x(self):
        return self.__center_x
    
    def y(self):
        return self.__center_y
    
    def radius(self):
        return self.__radius

class Application:
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __init_main(self):
        self.__root = tk.Tk()
        self.__root.title("Вращающаяся точка")
    
    def __init_canvas(self):
        self.__canvas = tk.Canvas(self.__root, width=CANVAS_WIDTH,
                                               height=CANVAS_HEIGHT, 
                                               bg=CANVAS_COLOR)
        self.__canvas.pack()

    def __init_control_frame(self):
        self.__control_frame = tk.Frame(self.__root)
        self.__control_frame.pack(pady=10)

    def __init_change_speed(self):
        self.__speed_label = tk.Label(self.__control_frame, text="регулировка скорости")
        self.__speed_label.grid(row=0, 
                                column=0, 
                                padx=10)

        self.__speed_slider = tk.Scale(self.__control_frame, from_=1, 
                                                             to=10, 
                                                             orient="horizontal", 
                                                             command=self.__on_speed_change)
        self.__speed_slider.grid(row=0, 
                                 column=1, 
                                 padx=10)

    def __init_change_or_speed(self):
        self.__speed_or_label = tk.Label(self.__control_frame, text="Направление движения")
        self.__speed_or_label.grid(row=1, 
                                   column=0, 
                                   padx=10)

        self.__speed_or_slider = tk.Scale(self.__control_frame, from_=0, 
                                                                to=1, 
                                                                orient="horizontal", 
                                                                command=self.__on_speed_or_change)
        self.__speed_or_slider.grid(row=1, 
                                    column=1, 
                                    padx=10)

    def __init_draw_in_canvas(self):
        self.__circle = Circle()
        self.__angle = POINT_START_POSITION

        self.__canvas.create_oval(self.__circle.x() - self.__circle.radius(),
                                  self.__circle.y() - self.__circle.radius(),
                                  self.__circle.x() + self.__circle.radius(),
                                  self.__circle.y() + self.__circle.radius(),
                                  outline=CIRCLE_COLOR)

        self.__speed = POINT_SPEED
        self.__point = self.__canvas.create_oval(self.__circle.x() - POINT_RADIUS,
                                            self.__circle.y() - POINT_RADIUS,
                                            self.__circle.x() + POINT_RADIUS,
                                            self.__circle.y() + POINT_RADIUS, 
                                            fill=POINT_COLOR)
    def __initUI(self):
        self.__init_main()
        self.__init_canvas()
        self.__init_control_frame()
        self.__init_change_speed()
        self.__init_change_or_speed()
        self.__init_draw_in_canvas()

    def __animate(self):
        x = self.__circle.x() + self.__circle.radius() * math.cos(self.__angle)
        y = self.__circle.y() + self.__circle.radius() * math.sin(self.__angle)

        self.__canvas.coords(self.__point, x - POINT_RADIUS, 
                                           y - POINT_RADIUS,
                                           x + POINT_RADIUS,
                                           y + POINT_RADIUS)

        self.__angle += int(self.__speed) / 20
        self.__root.after(20, self.__animate)
    
    def __on_speed_change(self, new_speed):
        self.__speed = new_speed

    def __on_speed_or_change(self, or_speed):
        self.__speed = int(self.__speed) * (-1)

    def run(self):
        self.__animate()
        self.__root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
