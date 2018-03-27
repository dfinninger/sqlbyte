import asyncio

from src.sqlbyte import repl

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(repl.run())
    loop.close()
