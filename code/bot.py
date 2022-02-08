import discord
import os
from discord.ext import tasks

TOKEN = os.environ.get('BOT_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')

client = MyClient()
client.run(TOKEN)