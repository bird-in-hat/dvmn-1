import curses_tools
import asyncio
import os
import random


def get_frames():
    frames_path = os.path.dirname(os.path.abspath(__file__)) + "/frames/garbage/"
    return [curses_tools.get_file_content(frames_path + filename) for filename in os.listdir(frames_path)]


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        curses_tools.draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


def get_random_garbage(canvas, frames):
    rows_number, columns_number = canvas.getmaxyx()
    return fly_garbage(canvas, random.randrange(1, columns_number), random.choice(frames))