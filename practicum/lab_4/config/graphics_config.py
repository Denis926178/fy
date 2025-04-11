''' Содержит информацию об используемых картинках '''

from takeimages import *
from constants import *

background_win = 'icon/win.png'
background_fail = 'icon/over.jpg'

# graphic_filenames - список с информацией о картинках героев
# в нем лежат записи формата [имя картинки, масштаб (процентов)].
# Используем константы в качестве индексов, чтобы не путаться, 
# в каком месте списка кто должен оказаться. 
# Программа будет работать нормально при любом порядке добавления картинок, и любых значениях констант,
# если только gr_total больше любой другой.

graphic_filenames = list(range(gr_total)) # создает список нужной длины (в python 3 range() - это не список, надо переводить)

graphic_filenames[gr_hero] = ['icon/m1.png', 16]
graphic_filenames[gr_enemy] = ['icon/st1.png', 16]
graphic_filenames[gr_plat_l] = ['icon/plat_l.png', 30]
graphic_filenames[gr_plat_m] = ['icon/plat.png', 30]
graphic_filenames[gr_plat_r] = ['icon/plat_r.png', 30]
graphic_filenames[gr_fire] = ['icon/arrow.png', 16]
graphic_filenames[gr_enemyfire] = ['icon/stone1.png', 10]
graphic_filenames[gr_enemy2] = ['icon/varvar.png', 16]
graphic_filenames[gr_goal] = ['icon/door.png', 20]

def file_images():
    ''' возвращает список картинок, переведённых в нужный формат, масштабированных, с убранной прозрачной каймой.
    в списке вторая половина картинок - те же, что и в первой половине, но смотрят влево '''
    imagelist = []
    for info in graphic_filenames: # используем порядок картинок в списке graphic_filenames, он уже согласован с константами типа gr_enemy, gr_hero
        filename = info[0]
        size = info[1]
        img = crop_img(filename, size)
        imagelist.append(img)

    for i in range(gr_total):
        imagelist.append(pygame.transform.flip(imagelist[i], True, False)) # отражает по оси X, картинка смотрит влево

    return imagelist

