import asyncio
import curses_tools


frame_1 = None
frame_2 = None

ship_speed = 4


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

    ship_height, ship_width = curses_tools.get_frame_size(frame_1)

    if rows_direction < 0:
        row = max(1, row + rows_direction * ship_speed)
    if rows_direction > 0:
        row = min(row + rows_direction * ship_speed, max_row - ship_height)

    if columns_direction < 0:
        column = max(1, column + columns_direction * ship_speed)
    if columns_direction > 0:
        column = min(column + columns_direction * ship_speed, max_column - ship_width)

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