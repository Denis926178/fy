from PIL import Image, ImageTk

class Explosion:
    __explosion_frames_cache = None
    __size = 50

    def __init__(self, canvas, x, y):
        self.__canvas = canvas
        self.__x = x
        self.__y = y
        self.size = 50

        if Explosion.__explosion_frames_cache is None:
            self.__load_explosion_frames()
        
        self.__explosion_frames = Explosion.__explosion_frames_cache
        self.__current_frame = 0
        self.__current_frame_id = None

        self.__animate_explosion()

    @classmethod
    def __load_explosion_frames(cls):
        explosion_image = Image.open("./icons/pngwing.com.png")
        frame_width = 256
        frame_height = 256

        cls.__explosion_frames_cache = []
        for row in range(0, 6, 2):
            for col in range(0, 8, 2):
                frame = explosion_image.crop((
                    col * frame_width,
                    row * frame_height,
                    (col + 1) * frame_width,
                    (row + 1) * frame_height
                ))
                resized_frame = frame.resize((cls.__size, cls.__size), Image.ANTIALIAS)
                cls.__explosion_frames_cache.append(ImageTk.PhotoImage(resized_frame))

    def __animate_explosion(self):
        if self.__current_frame_id is not None:
            self.__canvas.delete(self.__current_frame_id)

        if self.__current_frame >= len(self.__explosion_frames):
            return

        frame = self.__explosion_frames[self.__current_frame]
        self.__current_frame_id = self.__canvas.create_image(self.__x, self.__y, image=frame)
        self.__current_frame += 2

        self.__canvas.after(20, self.__animate_explosion)
