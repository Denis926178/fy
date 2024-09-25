import tkinter as tk

def on_speed_change(val):
    # Здесь можно обработать изменение скорости
    print(f"Скорость: {val}")

root = tk.Tk()
root.title("Схема с регулировкой скорости")

# Создаем Canvas в верхней части экрана
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Создаем Frame для размещения текста и регулировщика
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Надпись "регулировка скорости" слева
speed_label = tk.Label(control_frame, text="регулировка скорости")
speed_label.grid(row=0, column=0, padx=10)

# Ползунок для регулировки скорости справа
speed_slider = tk.Scale(control_frame, from_=1, to=10, orient="horizontal", command=on_speed_change)
speed_slider.grid(row=0, column=1, padx=10)

root.mainloop()
