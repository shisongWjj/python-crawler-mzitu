# 对专辑标题生成词云
import asyncio

import aiomysql
import jieba
from jieba import analyse
from matplotlib import pyplot
from wordcloud import WordCloud


def generate(text):
    # 添加字典
    jieba.load_userdict(r'../assets/jieba.txt')
    # 添加自定义分词
    # [jieba.add_word(k) for k in []]
    # 删除不必要分词
    [jieba.del_word(k) for k in ['十足', '令人', '尽显', '演绎']]

    # https://github.com/fxsjy/jieba#基于-tf-idf-算法的关键词抽取
    # 取Top30，生成直方图，返回是一个Tuple列表，其中权重以小数表示
    tags = analyse.extract_tags(text, topK=30, withWeight=True, )
    # 为了便于计算，将权重乘以100转换为百分数，方便使用Excel生成图表
    [print(item[0], '\t', int(item[1] * 100)) for item in tags]

    # 取Top100的词生成词云
    tags = analyse.extract_tags(text, topK=100, withWeight=False)
    new_text = ' '.join(tags)
    print(new_text)

    # 对分词文本生成词云
    # 生成词云，需要指定支持中文的字体，否则无法生成中文词云
    wc = WordCloud(
        # 设置词云中字号最大值
        # max_font_size=120,
        # min_font_size=24,
        # 设置词云图片宽、高
        width=1024,
        height=576,
        # 设置词云文字字体(美化和解决中文乱码问题)
        font_path=r'../assets/fonts/msyh.ttf'
    ).generate(new_text)

    # 绘图(标准长方形图)
    pyplot.imshow(wc, interpolation='bilinear')
    pyplot.figure()
    pyplot.axis('off')
    # 将图片输出到文件
    wc.to_file(r'../assets/images/wc.png')


async def main(loop):
    async with aiomysql.create_pool(host='192.168.0.105', port=3306,
                                    user='root', password='123456',
                                    db='mzitu', loop=loop,
                                    minsize=5, maxsize=20) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # 查询全部专辑名称，组装后进行中文分词
                await cursor.execute("SELECT `name` FROM album")
                text = ' '.join([items[0] for items in await cursor.fetchall()])

                # 一共 24605 个字符(含拼接时生产的空格)
                # print(len(text))
                # print(text)

                # 生成词云
                generate(text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop();
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()
