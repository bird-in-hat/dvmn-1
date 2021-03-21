import asyncio
import aiofiles
from datetime import datetime
import argparse
import os
import logging

logging.basicConfig(level=logging.DEBUG)


async def listen_chat(host: str, port: int, history_path: str):
    reader, writer = await asyncio.open_connection(
        host, port)

    while data := await reader.read(1000):
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        msg = f'[{now}] {data.decode()}'
        async with aiofiles.open(history_path, mode='a', encoding='utf-8') as myfile:
            await myfile.write(msg)

    logging.info('Close the connection')
    writer.close()


def get_arg_parser():
    parser = argparse.ArgumentParser(description="Async chat")
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--history', default=None)
    return parser


if __name__ == '__main__':
    args = get_arg_parser().parse_args()
    host = args.host or os.getenv('HOST', 'minechat.dvmn.org')
    port = args.port or os.getenv('PORT', 5000)
    history_path = args.history or os.getenv('HISTORY', '~/minechat.history')
    asyncio.run(listen_chat(host, port, history_path))
