import curses_tools
import asyncio
import os
import random
from obstacles import Obstacle
from explosion import explode
import state
from game_scenario import get_garbage_delay_tics


def get_frames():
    frames_path = os.path.dirname(os.path.abspath(__file__)) + "/frames/garbage/"
    return [curses_tools.get_file_content(frames_path + filename) for filename in os.listdir(frames_path)]


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number)
    row = 1
    height, width = curses_tools.get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, rows_size=height, columns_size=width)
    _, bounding_column, bounding_frame = obstacle.dump_bounding_box()

    state.obstacles.append(obstacle)

    while obstacle.row < rows_number:
        # curses_tools.draw_frame(canvas, obstacle.row - 1, bounding_column, bounding_frame)
        curses_tools.draw_frame(canvas, obstacle.row, column, garbage_frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, obstacle.row, column, garbage_frame, negative=True)
        # curses_tools.draw_frame(canvas, obstacle.row - 1, bounding_column, bounding_frame, negative=True)
        obstacle.row += speed

        if obstacle in state.obstacles_in_last_collisions.copy():
            state.obstacles_in_last_collisions.remove(obstacle)
            state.obstacles.remove(obstacle)

            state.coroutines.append(explode(canvas, obstacle.row + height // 2, column + width // 2))

            return


def get_random_garbage(canvas, frames):
    """Returns coroutine
    """
    rows_number, columns_number = canvas.getmaxyx()
    frame = random.choice(frames)
    column = random.randrange(0, columns_number)
    speed = random.choice([0.3, 0.4, 0.5, 0.6])
    return fly_garbage(canvas, column, frame, speed)


async def fill_orbit_with_garbage(canvas, frames):
    state.coroutines.append(get_random_garbage(canvas, frames))

    tics = 0
    while True:
        tics_delay = get_garbage_delay_tics(state.year) 
        if tics_delay and tics_delay <= tics:
            tics = 0
            state.coroutines.append(get_random_garbage(canvas, frames))

        for o in state.coroutines.copy():
            try:
                o.send(None)
            except StopIteration:
                state.coroutines.remove(o)
        tics += 1
        await asyncio.sleep(0)
