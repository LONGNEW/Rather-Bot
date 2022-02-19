import discord, looping, os

class MyClient(discord.Client):
    async def on_ready(self):
        self.task = looping.MyCog()
        await client.change_presence(activity=discord.Game("근무"))
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == "연결":
            looping.status()
            print(f"{message.guild.name} typed [연결]")
            for ch in self.task.channels.keys():
                print(ch.id, ch, ch.guild.name)

        if message.content == '공지':
            # 새로운 채널이 연결된 경우 이를 저장.
            if message.channel not in self.task.channels:
                self.task.channels[message.channel] = 1

            print(f"{message.guild.name} typed [공지]")
            for ch in self.task.channels.keys():
                print(ch.id, ch, ch.guild.name)

            await self.change_presence(activity=discord.Game("근무"))
            await message.channel.send(f"added [{message.guild.name}]")

        if message.content == '정지':
            del self.task.channels[message.channel]

            print(f"{message.guild.name} typed [정지]")
            for ch in self.task.channels.keys():
                print(ch.id, ch)

            await message.channel.send(f"added [{message.guild.name}]")


# TOKEN = os.environ.get('BOT_TOKEN')
client = MyClient()
client.run("ODU2MTI4OTg1NDU1Nzg4MDMz.YM8iQA.LjgrT4m5OzEmWW0mi7Imv_c_rTU")