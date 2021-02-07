from aiohttp import web
import asyncio
import os
import aiofiles


INTERVAL_SECS = 1
FILES_ROOT = 'lesson_3/test_photos'


async def _archivate(archive_hash):
    archive_path = f'{FILES_ROOT}/{archive_hash}'

    proc = await asyncio.create_subprocess_shell(
        f"cd {archive_path} && zip - *",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    buffer_size = 500 * 1024
    while stdout := await proc.stdout.read(buffer_size):
        yield stdout


async def archivate(request):
    # raise NotImplementedError
    response = web.StreamResponse()
    archive_hash = request.match_info['archive_hash']
    archive_path = f'{FILES_ROOT}/{archive_hash}'
    if not os.path.isdir(archive_path):
        return web.HTTPNotFound(text="Archive not found")
    # Большинство браузеров не отрисовывают частично загруженный контент, только если это не HTML.
    # Поэтому отправляем клиенту именно HTML, указываем это в Content-Type.
    response.headers['Content-Type'] = 'application/zip, application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={archive_hash}.zip'

    try:
        # Отправляет клиенту HTTP заголовки
        await response.prepare(request)

        async for data in _archivate(archive_hash):
            await response.write(data)
        await response.write_eof()
    except Exception as e:
        return web.HTTPServerError()


async def handle_index_page(request):
    async with aiofiles.open('lesson_3/index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archivate),
    ])
    web.run_app(app, port=8001)
