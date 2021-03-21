import asyncio
import argparse
import os
import logging
import json
import aiofiles
from typing import Tuple

logging.basicConfig(level=logging.DEBUG)

TOKEN_PATH = 'token.txt'


async def register(reader: asyncio.StreamReader,
                   writer: asyncio.StreamWriter,
                   nickname: str) -> None:

    try:
        await reader.readline()  # skip greetings
        writer.write('\n'.encode())
        await reader.readline()

        writer.write(f'{nickname}\n'.encode())
        await writer.drain()
        token_response = await reader.readline()
        token = json.loads(token_response.decode())['account_hash']

        async with aiofiles.open(TOKEN_PATH, mode='w', encoding='utf-8') as tokenfile:
            await tokenfile.write(token)
    except Exception as err:
        logging.exception(f"{err}")
        raise

    return True


class InvalidTokenError(Exception):
    pass


class NeedRegistrationError(Exception):
    pass


async def get_connection(host, port) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    return await asyncio.open_connection(host, port)


async def get_token_from_file() -> str:
    if os.path.isfile(TOKEN_PATH):
        async with aiofiles.open(TOKEN_PATH, mode='r', encoding='utf-8') as myfile:
            return await myfile.readline()
    else:
        raise NeedRegistrationError()


async def authorise(reader: asyncio.StreamReader,
                    writer: asyncio.StreamWriter,
                    token: str = None) -> None:
    await reader.readline()  # skip greetings
    writer.write(f'{token}\n'.encode())
    token_response = await reader.readline()
    logging.debug(f'Authorization: {token_response.decode()}')
    token_response = json.loads(token_response.decode())
    if 'nickname' in token_response and 'account_hash' in token_response:
        await reader.readline()
        return
    else:
        raise InvalidTokenError()



async def submit_message(reader: asyncio.StreamReader,
                         writer: asyncio.StreamWriter, 
                         msg: str):
    try:
        _msg = msg.replace(r'\n','')
        writer.write(f"{_msg}\n\n".encode())
        await writer.drain()
        response = await reader.readline()
        logging.info("Msg response " + response.decode())
    except Exception as err:
        logging.debug(f'Error: {err}')


async def serve(host: str, port: int, message: str, nickname: str = None, token: str = None):
    try:
        reader, writer = await get_connection(host, port)
    except Exception as err:
        logging.exception(f"Connection error: {err}")
        return

    try:
        if not token:
            token = await get_token_from_file()
        await authorise(reader, writer, token)
    except (InvalidTokenError, NeedRegistrationError):
        if not nickname:
            raise NeedRegistrationError('Provide nickname to register')
        else:
            await register(reader, writer, nickname)
    except Exception as err:
        logging.exception(f"Authorisation error: {err}")
        return

    await submit_message(reader, writer, message)


def get_arg_parser():
    parser = argparse.ArgumentParser(description="Async chat")
    parser.add_argument('-m','--message', type=str, required=True)
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--nickname', type=str)
    parser.add_argument('--token', type=str)
    return parser


if __name__ == '__main__':
    args = get_arg_parser().parse_args()
    host = args.host or os.getenv('HOST', 'minechat.dvmn.org')
    port = args.port or os.getenv('PORT', 5050)
    nickname = args.nickname or None
    token = args.token or None
    asyncio.run(serve(host, port, args.message, nickname, token))
