import os
import asyncio
import discord
from dotenv import load_dotenv
from time import sleep
from random import getrandbits


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
HEALTHCHECK_INTERVAL = int(os.getenv('HEALTHCHECK_INTERVAL'))


class Client(discord.Client):
    def __init__(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        super().__init__()
        self.loop.create_task(self.healthcheck())

    async def on_ready(self):
        print(f"Connected as '{self.user.name}' (id: {self.user.id}).")

    async def healthcheck(self):
        await self.wait_until_ready()
        await asyncio.sleep(2)
        while not self.is_closed():             
            if not is_healthy():
                print('Closing connection.')
                await self.close()
            await asyncio.sleep(HEALTHCHECK_INTERVAL)


def is_healthy():
    # TODO: Add real api healthcheck here
    healthy = bool(getrandbits(1))
    print(f'Healthy? { "yes" if healthy else "no" }')
    return healthy


if __name__ == '__main__':
    while True:
        if is_healthy():
            if os.fork() == 0: 
                # child
                client = Client()
                client.run(TOKEN)
                exit(0)
            else: 
                # parent
                os.wait()
        sleep(HEALTHCHECK_INTERVAL)
