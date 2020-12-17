import asyncio
import curses_tools
import settings
import itertools


def get_ship_coordinates(canvas, row, column, frame):
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)

    ship_height, ship_width = curses_tools.get_frame_size(frame)

    if rows_direction < 0:
        row = max(1, row + rows_direction * settings.SHIP_SPEED)
    if rows_direction > 0:
        row = min(row + rows_direction * settings.SHIP_SPEED, max_row - ship_height)

    if columns_direction < 0:
        column = max(1, column + columns_direction * settings.SHIP_SPEED)
    if columns_direction > 0:
        column = min(column + columns_direction * settings.SHIP_SPEED, max_column - ship_width)

    return row, column, space_pressed


async def animate_spaceship(canvas, row, column, frames):
    for frame in itertools.cycle(frames):
        row, column, space_pressed = get_ship_coordinates(canvas, row, column, frame)
        curses_tools.draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, frame, negative=True)
