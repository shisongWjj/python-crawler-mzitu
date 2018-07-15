import asyncio
import os

import aiohttp


async def download_page(session, url):
    """
    下载网页
    :param session:
    :param url:
    :return:
    """
    # https://docs.aiohttp.org/en/stable/client_reference.html#basic-api
    # https://docs.aiohttp.org/en/stable/client_reference.html#response-object
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.text(encoding='utf-8')
        else:
            print('status = {}, reason = {}'.format(resp.status, resp.reason))
            resp.raise_for_status()


async def download_image(session, url):
    """
    下载图片
    :param session:
    :param url:
    :return:
    """
    # https://docs.aiohttp.org/en/stable/client_reference.html#response-object
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.read()
        else:
            print('status = {}, reason = {}'.format(resp.status, resp.reason))
            resp.raise_for_status()


if __name__ == '__main__':
    """
    测试逻辑
    """

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://www.mzitu.com/'
    }


    async def main(_loop):
        # https://docs.aiohttp.org/en/stable/client_reference.html
        async with aiohttp.ClientSession(
                loop=_loop,
                headers=HEADERS,
                conn_timeout=3.0
        ) as session:
            # 下载网页，打印网页内容
            html = await download_page(session, r'http://www.mzitu.com/142026')
            print(html)

            # 下载图片，将图片写入磁盘
            image = await download_image(session, r'http://i.meizitu.net/2018/07/08c01.jpg')
            # 目录可能不存在，先创建目录
            if not os.path.exists('.data'):
                os.mkdir('.data')
            # 注意要以二进制文件形式打开
            with open('.data/08c01.jpg', 'bw+') as f:
                f.write(image)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
