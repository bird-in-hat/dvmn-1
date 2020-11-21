import time
import curses
from fire import fire
from star import get_star_coroutine
from spaceship import animate_spaceship


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    coroutines = []

    # Stars
    for i in range(100):
        coroutines.append(get_star_coroutine(canvas))

    o_r = curses.LINES // 2
    o_c = curses.COLS // 2

    # Fire
    # coroutines.append(fire(canvas, curses.LINES-1, curses.COLS//2, columns_speed=-0.3))

    # Spaceship
    coroutines.append(animate_spaceship(canvas, o_r, o_c))

    while coroutines:
        for c in coroutines.copy():
            try:
                c.send(None)
            except StopIteration:
                coroutines.remove(c)
        time.sleep(0.1)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)