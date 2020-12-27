import time
import curses
import asyncio
import random
import settings
from curses_tools import sleep_random


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep_random(2)

        canvas.addstr(row, column, symbol)
        await sleep_random(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep_random(0.5)

        canvas.addstr(row, column, symbol)
        await sleep_random(0.3)


def get_star_coroutine(canvas):
    row = random.randrange(1, curses.LINES-1)
    column = random.randrange(1, curses.COLS-1)
    symbol = random.choice('+*.o')
    return blink(canvas, row, column, symbol)
