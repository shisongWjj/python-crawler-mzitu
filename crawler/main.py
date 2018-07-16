import asyncio
import os
from asyncio import Queue

import aiohttp
# 启动URL
import aiomysql

from crawler.downloader import download_page, download_image
from crawler.file_utils import MyFileUtils
from crawler.page_parser import parse_html
from crawler.processor import save_album

start_url = 'http://www.mzitu.com/'
# start_url = 'http://www.mzitu.com/142026/3'

# 新URL队列
new_urls = Queue()
# 已抓取队列集合（用于去重，同时包含已处理和未处理的URL）
seen_urls = set()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/55.0.2883.87 Safari/537.36',
    'Referer': 'http://www.mzitu.com/'
}

ROOT_DIR = r'D:\Temporary\mzitu'

sem = asyncio.Semaphore(500)


async def append_urls(urls):
    """
    将URL列表追加到队列中
    :param urls:
    :return:
    """

    if not urls:
        return

    # 进入该函数的URL基本都已符合规则，不需要再过滤
    # 仅针对已处理过的URL去重即可
    for url in urls:
        if not url or not url.startswith('http://www.mzitu.com'):
            continue
        if url not in seen_urls:
            await new_urls.put(url)
            seen_urls.add(url)
    pass


async def consumer(session, pool, utils):
    url = await new_urls.get()
    print('got url: {}'.format(url))

    # 下载URL对应网页
    html = await download_page(session, url)
    if not html:
        return

    # 解析网页，返回一个字典数据结构
    data = await parse_html(url, html)
    if not data:
        return

    # 如果存在 list_page_urls 或 photo_page_urls 字段，将其加入队列中
    if 'list_page_urls' in data and data['list_page_urls']:
        asyncio.ensure_future(append_urls(data['list_page_urls']))

    if 'photo_page_urls' in data and data['photo_page_urls']:
        asyncio.ensure_future(append_urls(data['photo_page_urls']))

    # 如果存在专辑信息，将其写入数据库
    if 'album_info' not in data or not data['album_info']:
        return

    # 只有有专辑名称的字典才需要入库，因为存在只有编号字段的情况
    if 'name' in data['album_info']:
        asyncio.ensure_future(save_album(pool, data['album_info']))

    # 如果存在照片，将其下载下来并写入磁盘
    if 'image' in data and 'number' in data['album_info']:
        image_bytes = await download_image(session, data['image'])
        if image_bytes:
            utils.save_photo(os.path.join(ROOT_DIR, str(data['album_info']['number'])),
                             data['image'].split('/')[-1], image_bytes)

    pass


async def main(_loop):
    # 创建文件目录
    utils = MyFileUtils()
    utils.mkdirs(ROOT_DIR)

    # 初始化队列
    await new_urls.put(start_url)
    seen_urls.add(start_url)

    async with aiohttp.ClientSession(
            loop=_loop,
            headers=HEADERS,
            conn_timeout=3.0
    ) as session:
        async with aiomysql.create_pool(host='192.168.0.105',
                                        port=3306,
                                        user='root',
                                        password='123456',
                                        db='mzitu',
                                        maxsize=200,
                                        minsize=10,
                                        loop=_loop) as pool:
            # 循环从队列中取出URL进行爬取操作
            while True:
                # sem 控制并发量
                async with sem:
                    # 这里使用 asyncio.ensure_future() 程序不执行，原因尚不清楚
                    # asyncio.ensure_future(consumer(session, pool, utils))
                    # 改用原来的方法执行
                    await consumer(session, pool, utils)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(main(loop))
        loop.run_forever()
    finally:
        loop.close()
