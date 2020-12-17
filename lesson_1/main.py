import time
import curses
from fire import fire
from star import get_star_coroutine
from spaceship import animate_spaceship
from curses_tools import get_file_content
import settings
import os 



def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    # Stars
    star_coroutines = [get_star_coroutine(canvas) for i in range(50)]

    lines_center = curses.LINES // 2
    cols_center = curses.COLS // 2

    animation_coroutines = []
    # Fire
    # animation_coroutine.append(fire(canvas, curses.LINES-1, curses.COLS//2, columns_speed=-0.3))

    # Spaceship
    ship_frames = (get_file_content(os.path.dirname(os.path.abspath(__file__)) + "/animation/rocket_frame_{}.txt".format(i)) for i in [1, 2])
    ship_coroutine = animate_spaceship(canvas, lines_center, cols_center, ship_frames)

    while True:
        ship_coroutine.send(None)

        for sc in star_coroutines:
            sc.send(None)

        for ac in animation_coroutines.copy():
            try:
                ac.send(None)
            except StopIteration:
                animation_coroutines.remove(ac)

        canvas.refresh()
        time.sleep(settings.TIC_RATE)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)