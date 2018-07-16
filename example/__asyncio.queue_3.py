# 生产者、消费者

import asyncio


async def producer(queue, name, consumer_nums):
    print('producer {}: starting'.format(name))

    # 生产者生产10条数据
    for i in range(10):
        await queue.put(i)
        print('producer {}: put {}'.format(name, i))

    # 发送结束信号，有几个消费者就要发几次
    [await queue.put(None) for _ in range(consumer_nums)]

    print('producer {}: completed'.format(name))

    await queue.join()

    print('exit ...')


async def consumer(queue, name):
    print('consumer {}: starting'.format(name))

    while True:
        item = await queue.get()
        if item is None:
            # 每次消费都执行一次，实际是一个计数递减的过程
            queue.task_done()
            break
        else:
            print('consumer {}: got {}'.format(name, item))
            await asyncio.sleep(0.03)
            # 每次消费都执行一次，实际是一个计数递减的过程
            queue.task_done()

    print('consumer {}: completed'.format(name))


async def main(_loop):
    # 消费者数量
    num = 3

    queue = asyncio.Queue()

    # 消费者有多个
    consumers = [
        consumer(queue, 'cons_{}'.format(i + 1))
        for i in range(num)
    ]

    # 生产者只有一个
    prod = producer(queue, 'prod', num)

    await asyncio.wait(consumers + [prod])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()
