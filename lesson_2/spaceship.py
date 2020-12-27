import asyncio
import curses_tools
import settings
import itertools
import os
from physics import update_speed


row_speed = 0
column_speed = 0


def get_frames():
    curr_path = os.path.dirname(os.path.abspath(__file__))
    return [curses_tools.get_file_content(curr_path + "/frames/ship/rocket_frame_{}.txt".format(i)) for i in [1, 2]]


def get_ship_coordinates(canvas, row, column, frame):
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    global row_speed
    global column_speed

    rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)

    ship_height, ship_width = curses_tools.get_frame_size(frame)

    row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
    row, column = row + int(row_speed * settings.SHIP_ROW_SPEED), column + int(column_speed * settings.SHIP_COL_SPEED)

    if row < 1:
        row = 1
    if row > max_row - ship_height:
        row = max_row - ship_height

    if column < 1:
        column = 1
    if column > max_column - ship_width:
        column = max_column - ship_width

    return row, column, space_pressed


async def animate_spaceship(canvas, row, column, frames):
    for frame in itertools.cycle(frames):
        row, column, space_pressed = get_ship_coordinates(canvas, row, column, frame)
        curses_tools.draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, frame, negative=True)
