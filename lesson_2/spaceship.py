import asyncio
import curses_tools
import settings
import itertools
import os
import state
from physics import update_speed
from fire import fire


row_speed = 0
column_speed = 0


class GameOverException(Exception):
    pass


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

    row = max(1, row)
    row = min(row, max_row - ship_height - 1)

    column = max(1, column)
    column = min(column, max_column - ship_width)

    return row, column, space_pressed


def animate_fire(canvas, shots):
    for s in shots.copy():
        try:
            s.send(None)
        except StopIteration:
            shots.remove(s)
    return shots


async def animate_spaceship(canvas, row, column, frames):
    shots = []
    height, width = curses_tools.get_frame_size(frames[0])
    for frame in itertools.cycle(frames):
        row, column, space_pressed = get_ship_coordinates(canvas, row, column, frame)
        curses_tools.draw_frame(canvas, row, column, frame)
        if space_pressed and state.shotgun_enabled:
            shots.append(fire(canvas, row, column + 2, rows_speed=-0.5))
        shots = animate_fire(canvas, shots)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, frame, negative=True)

        for obstacle in state.obstacles:
            if obstacle.has_collision(row, column, obj_size_rows=height, obj_size_columns=width):
                state.obstacles_in_last_collisions.append(obstacle)
                raise GameOverException()
