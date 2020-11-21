import asyncio
import curses_tools


HEIGHT = 9
WIDTH = 3

frame_1 = None
frame_2 = None


def load_frames():
    global frame_1, frame_2
    with open("animation/rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("animation/rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()


def check_move(canvas, row, column):
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)

    if 0 < row < max_row and 0 < column < max_column:
        row += rows_direction
        column += columns_direction
    return row, column, space_pressed


async def animate_spaceship(canvas, row, column):
    while True:
        curses_tools.draw_frame(canvas, row, column, frame_1)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, frame_1, negative=True)
        curses_tools.draw_frame(canvas, row, column, frame_2)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, frame_2, negative=True)

        row, column, space_pressed = check_move(canvas, row, column)


load_frames()