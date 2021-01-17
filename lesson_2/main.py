import time
import curses
from fire import fire
from star import get_star_coroutine
import spaceship
import space_garbage
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
    # Initial Fire
    # animation_coroutine.append()

    # Spaceship
    ship_frames = spaceship.get_frames()
    ship_coroutine = spaceship.animate_spaceship(canvas, lines_center, cols_center, ship_frames)

    # Garbage
    garbage_frames = space_garbage.get_frames()
    garbage_coroutine = space_garbage.fill_orbit_with_garbage(canvas, garbage_frames, 10)

    while True:
        ship_coroutine.send(None)

        for sc in star_coroutines:
            sc.send(None)

        for ac in animation_coroutines.copy():
            try:
                ac.send(None)
            except StopIteration:
                animation_coroutines.remove(ac)

        garbage_coroutine.send(None)

        canvas.refresh()
        time.sleep(settings.TIC_RATE)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)