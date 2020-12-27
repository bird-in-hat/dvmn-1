import curses_tools
import asyncio
import os
import random


class Obstacle:
    def __init__(self, coroutine, column, frame, speed=0.5):
        self.coroutine = coroutine
        self.column = column
        self.frame = frame
        self.speed = speed


obstacles = []


def get_frames():
    frames_path = os.path.dirname(os.path.abspath(__file__)) + "/frames/garbage/"
    return [curses_tools.get_file_content(frames_path + filename) for filename in os.listdir(frames_path)]


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1

    while row < rows_number:
        curses_tools.draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


def get_random_garbage(canvas, frames):
    """Returns Obstacle 
    """
    rows_number, columns_number = canvas.getmaxyx()
    column = random.randrange(1, columns_number)
    frame = random.choice(frames)
    speed = random.choice([0.3, 0.4, 0.5, 0.6])
    coro = fly_garbage(canvas, column, frame, speed)
    return Obstacle(coro, column, frame, speed)


async def fill_orbit_with_garbage(canvas, frames, obsctacles_count=10):
    global obstacles

    for i in range(obsctacles_count // 2):
        obstacles.append(get_random_garbage(canvas, frames))

    while True:
        if len(obstacles) < obsctacles_count and random.random() < 0.1:
            obstacles.append(get_random_garbage(canvas, frames))
        for o in obstacles.copy():
            try:
                o.coroutine.send(None)
            except StopIteration:
                obstacles.remove(o)
                # # Replace excluded with new
                obstacles.append(get_random_garbage(canvas, frames))
        await asyncio.sleep(0)
