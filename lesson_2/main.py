import time
import curses
from fire import fire
from star import get_star_coroutine
import spaceship
import space_garbage
from curses_tools import get_file_content, update_state, show_year_info
import settings
import os 
from game_over import game_over_draw


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    # Stars
    star_coroutines = [get_star_coroutine(canvas) for i in range(50)]

    lines_center = curses.LINES // 2
    cols_center = curses.COLS // 2

    update_state_coroutine = update_state()
    show_year_coroutine = show_year_info(canvas)

    # Spaceship
    ship_frames = spaceship.get_frames()
    ship_coroutine = spaceship.animate_spaceship(canvas, lines_center, cols_center, ship_frames)

    # Garbage
    garbage_frames = space_garbage.get_frames()
    garbage_coroutine = space_garbage.fill_orbit_with_garbage(canvas, garbage_frames)

    while True:
        try:
            ship_coroutine.send(None)
        except spaceship.GameOverException:
            canvas.clear()
            game_over_draw(canvas)
            canvas.refresh()
            break

        for sc in star_coroutines:
            sc.send(None)

        garbage_coroutine.send(None)
        update_state_coroutine.send(None)
        show_year_coroutine.send(None)

        canvas.refresh()
        time.sleep(settings.TIC_RATE)

    time.sleep(20)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)