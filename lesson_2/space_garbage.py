import curses_tools
import asyncio
import os
import random


class Obstacle:
    def __init__(self, frame, column, row, height, width, speed=0.5):
        self.frame = frame
        self.column = column
        self.row = row
        self.height = height
        self.width = width
        self.speed = speed

    def get_bounding_frame(self):
        frame = ' ' + '-' * (self.width - 1) + ' \n'
        for _ in range(self.height - 2):
            frame += '|' + ' ' * (self.width - 1) + '|\n'
        frame += ' ' + '-' * (self.width -1) + ' \n'
        return frame


obstacles = []


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
    obstacle = Obstacle(garbage_frame, column, row, height=height, width=width, speed=speed)
    bounding_frame = obstacle.get_bounding_frame()

    global obstacles
    obstacles.append(obstacle)

    while row < rows_number:
        curses_tools.draw_frame(canvas, row, column, bounding_frame)
        curses_tools.draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, row, column, garbage_frame, negative=True)
        curses_tools.draw_frame(canvas, row, column, bounding_frame, negative=True)
        row += speed
        obstacle.row = row


def get_random_garbage(canvas, frames):
    """Returns coroutine
    """
    rows_number, columns_number = canvas.getmaxyx()
    frame = random.choice(frames)
    column = random.randrange(0, columns_number)
    speed = random.choice([0.3, 0.4, 0.5, 0.6])
    return fly_garbage(canvas, column, frame, speed)


async def fill_orbit_with_garbage(canvas, frames, obsctacles_count=10):
    coroutines = []

    for i in range(obsctacles_count // 3):
        coroutines.append(get_random_garbage(canvas, frames))

    while True:
        if len(coroutines) < obsctacles_count and random.random() < 0.13:
            coroutines.append(get_random_garbage(canvas, frames))

        for o in coroutines.copy():
            try:
                o.send(None)
            except StopIteration:
                coroutines.remove(o)
        await asyncio.sleep(0)
