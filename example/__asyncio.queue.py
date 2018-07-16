import asyncio
from asyncio import Queue

queue = Queue()

# <class 'asyncio.queues.Queue'> <Queue maxsize=0>
print(type(queue), queue)


async def main():
    # False True
    print(queue.full(), queue.empty())

    await queue.put(1)
    await queue.put(2)
    await queue.put(3)
    # <Queue maxsize=0 _queue=[1, 2, 3] tasks=3>
    print(queue)

    # 发现没有检查元素存在的方法，所以只能单纯做队列使用
    # 做爬虫时还得配合其它的数据结构实现URL队列管理（去重）

    # False False
    print(queue.full(), queue.empty())
    # 1
    print(await queue.get())
    # 2
    print(await queue.get())
    # 1
    print(queue.qsize())
    # 3
    print(await queue.get())
    # False True
    print(queue.full(), queue.empty())

    # 如果队列空了，继续取会怎样？
    # 结论：队列空了，继续取会阻塞住
    # print('队列已经空了')
    # print(await queue.get())
    # print('程序卡住了吧 。。。')

    # put_nowait / get_nowait ，是阻塞方法
    queue.put_nowait('a')
    queue.put_nowait('b')
    queue.put_nowait('c')

    # a
    print(queue.get_nowait())
    # b
    print(queue.get_nowait())
    # c
    print(queue.get_nowait())
    # False True
    print(queue.full(), queue.empty())

    # 阻塞队列，直到队列所有项被取走，即队空
    # await queue.join()

    # 指示队列中的任务已完成，如果此时队列被join()阻塞着，此方法表示程序执行（解除阻塞状态）
    # queue.task_done()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
