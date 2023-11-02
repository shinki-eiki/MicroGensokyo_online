import asyncio

async def test():
    print('Test function.')

async def foo(char:str, count: int):
    for i in range(count):
        print(f"{char}-{i}")
        await asyncio.sleep(1)


async def main():
    await test()
    print('Main begins.')
    task1 = asyncio.create_task(foo("A", 2))
    task2 = asyncio.create_task(foo("B", 3))
    task3 = asyncio.create_task(foo("C", 2))

    print('Tasks had benn created.')
    await asyncio.sleep(3)
    print('After 3 seconds...')
    print(type(task1))
    await task1
    print('task1 done.')
    await task2
    print('task2 done.')
    await task3
    print('task3 done.')

if __name__ == '__main__':
    # task = asyncio.create_task(foo('None', 1))
    # await task
    asyncio.run(main())