import os
import asyncio
import discord
import requests
from dotenv import load_dotenv
from time import sleep
from random import getrandbits


load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
HEALTHCHECK_INTERVAL = int(os.getenv('HEALTHCHECK_INTERVAL'))
HEALTHCHECK_URL = os.getenv('HEALTHCHECK_URL')

class Client(discord.Client):
    def __init__(self):
        # idempotent loop reinitialization, since using fork() with asyncio
        # https://bugs.python.org/issue21998
        asyncio.set_event_loop(asyncio.new_event_loop())
        super().__init__()
        self.loop.create_task(self.healthcheck())

    async def on_ready(self):
        print(f"Connected as '{self.user}' (id: {self.user.id}).")

    async def healthcheck(self):
        await self.wait_until_ready()
        while not self.is_closed():             
            if not is_server_healthy():
                print('Closing connection.')
                await self.close()
            await asyncio.sleep(HEALTHCHECK_INTERVAL)


def is_server_healthy():
    # TODO: Add real api healthcheck here
    response = requests.get(
        url = HEALTHCHECK_URL,
    )
    if response.status_code == 200:
        print('Healthcheck: success')
        return True
    print('Healthcheck: failure')
    return False


if __name__ == '__main__':
    while True:
        if is_server_healthy():
            # run disord.py's Client() in a separate process
            # due to the use of `set_wakeup_fd` which can only
            # be called from the main thread of the main interpreter
            # https://docs.python.org/3/library/signal.html#signal.set_wakeup_fd
            if os.fork() == 0: 
                # child
                client = Client()
                client.run(DISCORD_TOKEN)
                exit(0)
            
            # parent
            os.wait()
        sleep(HEALTHCHECK_INTERVAL)
