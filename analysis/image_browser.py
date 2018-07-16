# 实现一个简易版图片浏览器
# http://localhost:8080/
import os

import aiomysql
from aiohttp import web

routes = web.RouteTableDef()
root_dir = r'D:\Temporary\mzitu'


@routes.get('/')
async def _index(request):
    html = "<ul>"

    # 读取数据库
    async with request.app['pool'].acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM album ORDER BY number DESC")
            results = await cursor.fetchall()
            for r in results:
                html += "<li><a href='/{}' target='_blank'>{}</a></li>\n".format(r[1], r[2])
    html += "</ul>"

    return web.Response(text=html, content_type='text/html')


@routes.get('/{number}')
async def _album(request):
    number = request.match_info['number']
    # 遍历指定目录下的图片
    path = os.path.join(root_dir, number)

    html = ''
    for img in os.listdir(path):
        html += '<img src="/{}/{}" width="300" />\n'.format(number, img)

    return web.Response(text=html, content_type='text/html')


@routes.get('/{number}/{img}')
async def _photo(request):
    number = request.match_info['number']
    img = request.match_info['img']
    with open(os.path.join(root_dir, number, img), 'br') as f:
        return web.Response(body=f.read(), content_type='image/jpeg')
    return web.Response(body=None, content_type='image/jpeg')


async def init_pool(app):
    print('init database pool ...')
    app['pool'] = await aiomysql.create_pool(host='192.168.0.105', port=3306,
                                             user='root', password='123456',
                                             db='mzitu',
                                             minsize=5, maxsize=20)


async def destroy_pool(app):
    print('destroy database pool ...')
    await app['pool'].close()


if __name__ == '__main__':
    app = web.Application()

    app.on_startup.append(init_pool)
    app.on_shutdown.append(destroy_pool)

    app.add_routes(routes)
    web.run_app(app)
