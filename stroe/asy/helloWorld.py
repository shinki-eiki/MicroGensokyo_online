import asyncio


async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')
    return 'yes'
    # allow to return value

# a=main()
print(asyncio.run(main()))
print(asyncio.run(main()))
print('wait')
