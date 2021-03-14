from aiohttp import web
import asyncio
import os
import signal
import aiofiles
import logging
import argparse


DEFAULT_PHOTOS_PATH = 'lesson_3/test_photos'


async def archivate(request):
    # raise NotImplementedError
    response = web.StreamResponse()
    archive_hash = request.match_info['archive_hash']
    archive_path = f'{app["photos_path"]}/{archive_hash}'
    if not os.path.isdir(archive_path):
        return web.HTTPNotFound(text="Archive not found")

    # Большинство браузеров не отрисовывают частично загруженный контент, только если это не HTML.
    # Поэтому отправляем клиенту именно HTML, указываем это в Content-Type.
    response.headers['Content-Type'] = 'application/zip, application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={archive_hash}.zip'

    proc = await asyncio.create_subprocess_shell(
        f"cd {archive_path} && zip - *",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    # buffer_size = 500 * 1024
    buffer_size = 30 * 1024

    try:
        # Отправляет клиенту HTTP заголовки
        await response.prepare(request)

        while data := await proc.stdout.read(buffer_size):
            logging.info('Sending archive chunk')
            await response.write(data)
            if app['delay']:
                await asyncio.sleep(app['delay'])

        await response.write_eof()
        logging.info('Archive sent')
    except asyncio.CancelledError:
        response.force_close()
        logging.error('Download was cancelled')
        return web.HTTPServerError()
    except Exception as e:
        response.force_close()
        logging.error('Server error ' + str(e))
        return web.HTTPServerError()
    finally:
        if proc.returncode != 0:
            try:
                proc.kill()
                await proc.communicate()
            except Exception as e:
                logging.error("Exception killing proc " + str(e))


async def handle_index_page(request):
    async with aiofiles.open('lesson_3/index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


def get_arg_parser():
    parser = argparse.ArgumentParser(description="Micro service for downloading files")
    parser.add_argument('-l', '--logging', action='store_true')
    parser.add_argument('-d', '--delay', type=float, default=None)
    parser.add_argument('-p', '--path', default=None)
    return parser


def set_up(app):
    args = get_arg_parser().parse_args()
    if args.logging or bool(os.getenv('LOGGING', False)):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    app['delay'] = args.delay or float(os.getenv('DELAY', 0.0))
    photos_path = args.path or os.getenv('PHOTOS_PATH', DEFAULT_PHOTOS_PATH)
    if photos_path[-1] == '/':
        photos_path = photos_path[:-1]
    app['photos_path'] = photos_path


if __name__ == '__main__':
    app = web.Application()
    set_up(app)
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archivate),
    ])
    web.run_app(app, port=8001)
