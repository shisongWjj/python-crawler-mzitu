import asyncio
import re

import aiohttp
from pyquery import PyQuery

from crawler.downloader import download_page


async def parse_html(url, html):
    # http://pyquery.readthedocs.io/en/latest/
    # 根据url判断列表页还是专辑页，除这两类URL外忽略之
    # 列表页 -> http://www.mzitu.com/page/4/
    #        -> http://www.mzitu.com/
    # 专辑页 -> http://www.mzitu.com/142026
    #        -> http://www.mzitu.com/142026/2

    pq = PyQuery(html)

    # 不同类型页面返回的数据可能不一致，所以这里用字典封装
    url_prefix = 'http://www.mzitu.com'
    if url == '{}/'.format(url_prefix) or \
            re.match(r'^{}/page/(\d+)/$'.format(url_prefix), url, re.I):
        # 解析列表页
        photo_page_urls, list_page_urls = await _parse_list_page(pq)
        return {'photo_page_urls': photo_page_urls, 'list_page_urls': list_page_urls}
    elif re.match(r'^{}/(\d+)$'.format(url_prefix), url, re.I):
        # 解析专辑页(图片页首页)
        album_info, photo_page_urls, image = await _parse_album_page(pq)
        return {'photo_page_urls': photo_page_urls, 'album_info': album_info, 'image': image}
    elif re.match(r'^{}/(\d+)/\d+$'.format(url_prefix), url, re.I):
        # 解析图片页
        _, photo_page_urls, image = await _parse_photo_page(pq)
        return {'photo_page_urls': photo_page_urls, 'image': image}
    else:
        return {}


async def _parse_list_page(pq):
    """
    从列表页中抽取专辑页链接列表和其它列表页链接列表
    :param pq:
    :return:
    """
    # 抽取列表页链接
    list_page_urls = {a.get('href').strip() for a in pq('nav.navigation.pagination a[href]')}

    # 抽取专辑页链接(但实际上专辑页本身是照片页的第一页，统一按照片页处理)
    # album_page_links = {a.get('href').strip() for a in pq('#pins > li > a[href]')}
    photo_page_urls = {a.get('href').strip() for a in pq('#pins > li > a[href]')}

    return photo_page_urls, list_page_urls


async def _parse_album_page(pq):
    """
    专辑页信息提取，返回专辑信息、照片页链接列表、专辑封面图片地址
    :param pq:
    :return:
    """

    # 照片页链接列表，排除第一个，是上一组
    photo_page_urls = {a.get('href').strip() for a in pq('div.pagenavi > a[href]:gt(0)')}
    # print(photo_page_urls)

    # 抽取专辑信息
    name = pq('h2.main-title').text().strip()
    category = pq('div.main-meta a[rel="category tag"]').text().strip()
    p_time = ' '.join(pq('div.main-meta span:eq(1)').text().strip().split(' ')[1:])
    views = ''.join(pq('div.main-meta span:eq(2)').text().strip().replace('次浏览', '').split(','))
    image = pq('div.main-image img[src]').attr('src').strip()
    # print(name, category, p_time, views, image)

    return {'name': name,
            'category': category,
            'publish_time': p_time,
            'views': views}, photo_page_urls, image


async def _parse_photo_page(pq):
    # 照片页链接列表
    photo_page_urls = {a.get('href').strip() for a in pq('div.pagenavi > a[href]')}
    # print(photo_page_urls)

    # 本页照片
    image = pq('div.main-image img[src]').attr('src').strip()
    # print(image)

    return None, photo_page_urls, image


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


    async def print_data(session, url):
        html = await download_page(session, url)
        data = await parse_html(url, html)
        print(data)


    async def main(_loop):
        async with aiohttp.ClientSession(
                loop=_loop,
                headers=HEADERS,
                conn_timeout=3.0
        ) as session:
            # 列表页：
            # {'photo_page_urls': {'http://www.mzitu.com/142649', 'http://www.mzitu.com/142103', 'http://www.mzitu.com/142026', 'http://www.mzitu.com/141471', 'http://www.mzitu.com/142274', 'http://www.mzitu.com/141689', 'http://www.mzitu.com/141843', 'http://www.mzitu.com/141645', 'http://www.mzitu.com/142409', 'http://www.mzitu.com/142189', 'http://www.mzitu.com/142143', 'http://www.mzitu.com/141566', 'http://www.mzitu.com/142233', 'http://www.mzitu.com/141609', 'http://www.mzitu.com/142051', 'http://www.mzitu.com/141796', 'http://www.mzitu.com/141730', 'http://www.mzitu.com/141887', 'http://www.mzitu.com/142355', 'http://www.mzitu.com/142311', 'http://www.mzitu.com/141930', 'http://www.mzitu.com/141416', 'http://www.mzitu.com/141969', 'http://www.mzitu.com/141525'}, 'list_page_urls': {'http://www.mzitu.com/page/3/', 'http://www.mzitu.com/page/2/', 'http://www.mzitu.com/page/4/', 'http://www.mzitu.com/page/186/'}}
            await print_data(session, r'http://www.mzitu.com/')
            # {'photo_page_urls': {'http://www.mzitu.com/141088', 'http://www.mzitu.com/140326', 'http://www.mzitu.com/140371', 'http://www.mzitu.com/140615', 'http://www.mzitu.com/141299', 'http://www.mzitu.com/141052', 'http://www.mzitu.com/140658', 'http://www.mzitu.com/140752', 'http://www.mzitu.com/140914', 'http://www.mzitu.com/140526', 'http://www.mzitu.com/140946', 'http://www.mzitu.com/140873', 'http://www.mzitu.com/141228', 'http://www.mzitu.com/140818', 'http://www.mzitu.com/140271', 'http://www.mzitu.com/140460', 'http://www.mzitu.com/141253', 'http://www.mzitu.com/141363', 'http://www.mzitu.com/141187', 'http://www.mzitu.com/141009', 'http://www.mzitu.com/140414', 'http://www.mzitu.com/140704', 'http://www.mzitu.com/141130', 'http://www.mzitu.com/140574'}, 'list_page_urls': {'http://www.mzitu.com/page/4/', 'http://www.mzitu.com/page/5/', 'http://www.mzitu.com/page/3/', 'http://www.mzitu.com/page/186/', 'http://www.mzitu.com/'}}
            await print_data(session, r'http://www.mzitu.com/page/2/')
            # 专辑页：
            # {'photo_page_urls': {'http://www.mzitu.com/142026/4', 'http://www.mzitu.com/142026/2', 'http://www.mzitu.com/142026/3', 'http://www.mzitu.com/142026/24'}, 'album_info': {'name': '元气少女苏菲菲裙下风光别致吸睛 偷拍角度令人兴奋', 'category': '性感妹子', 'publish_time': '2018-07-12 20:44', 'views': '73890'}, 'image': 'http://i.meizitu.net/2018/07/08c01.jpg'}
            await print_data(session, r'http://www.mzitu.com/142026')
            # 照片页：
            # {'photo_page_urls': {'http://www.mzitu.com/142026/5', 'http://www.mzitu.com/142026/3', 'http://www.mzitu.com/142026/4', 'http://www.mzitu.com/142026', 'http://www.mzitu.com/142026/24'}, 'image': 'http://i.meizitu.net/2018/07/08c02.jpg'}
            await print_data(session, r'http://www.mzitu.com/142026/2')
            # 无效页：
            # {}
            await print_data(session, r'http://www.mzitu.com/tag/toutiaogirls/')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
