from itertools import cycle
import curses_tools


frame_1 = None
frame_2 = None


def load_frames():
    global frame_1, frame_2
    with open("animation/rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("animation/rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()


async def animate_spaceship(canvas, row, column):
    while True:
        await curses_tools.sleep(0.1)
        curses_tools.draw_frame(canvas, row, column, frame_2, negative=True)
        curses_tools.draw_frame(canvas, row, column, frame_1)
        await curses_tools.sleep(0.1)
        curses_tools.draw_frame(canvas, row, column, frame_1, negative=True)
        curses_tools.draw_frame(canvas, row, column, frame_2)


load_frames()