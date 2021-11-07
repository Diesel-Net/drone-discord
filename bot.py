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
        for guild in self.guilds:
            if guild.name == GUILD:
                break
        print(f'{self.user} (id: {self.user.id}) is connected to {guild.name} (id: {guild.id})')

    async def healthcheck(self):
        await self.wait_until_ready()
        await asyncio.sleep(2)
        
        while not self.is_closed():             

            if not is_healthy():
                print('Closing Discord connection.')
                await self.close()

            await asyncio.sleep(HEALTHCHECK_INTERVAL)


def run_client_and_exit():
    print('Starting Discord connection.')
    client = Client()
    client.run(TOKEN)
    exit(0)


def fork_client_and_wait():
    if os.fork() == 0:
        run_client_and_exit()
    else:
        os.wait()


def is_healthy():
    # TODO: Add real api healthcheck here
    healthy = bool(getrandbits(1))
    print(f'Healthcheck: {healthy}')
    return healthy


def run():
    while True:
        if is_healthy():
            fork_client_and_wait()


if __name__ == '__main__':
    run()

