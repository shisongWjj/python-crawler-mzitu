# 内容处理
import asyncio
from datetime import datetime

import aiomysql


async def save_album(pool, album):
    """
    保存专辑数据到数据库
    :param album:
    :return:
    """
    if not album:
        return
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO album (`number`,`name`,`publish_time`,`category`,`tags`,`views`) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (album['number'], album['name'],
                 album['publish_time'], album['category'],
                 album['tags'], album['views']))
        await conn.commit()


if __name__ == '__main__':
    async def main(loop):
        async with aiomysql.create_pool(host='192.168.0.105',
                                        port=3306,
                                        user='root',
                                        password='123456',
                                        db='mzitu',
                                        maxsize=20,
                                        minsize=5,
                                        loop=loop) as pool:
            await save_album(pool, {
                'number': 10086,
                'name': '激情夏日，情迷沙滩',
                'publish_time': datetime(2018, 7, 15, 13, 0, 0),
                'category': '比基尼',
                'tags': '小清新,比基尼',
                'views': 10000
            })


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
