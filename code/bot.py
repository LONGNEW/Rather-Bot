import discord, looping, os

channels = looping.channels

class MyClient(discord.Client):
    async def on_ready(self):
        self.task = looping.MyCog()
        self.work = 1
        await client.change_presence(activity=discord.Game("근무"))
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '공지':
            # 새로운 채널이 연결된 경우 이를 저장.
            if message.channel not in channels:
                channels[message.channel] = 1

            # 근무를 하지 않고 있던 경우에는 재시작을 해서 메시지를 보내도록 해야함.
            if not self.work:
                self.work = 1
                await self.task.notice.start()

            print(f"{message.guild.name}에서 [공지]를 입력")
            for ch in channels.keys():
                print(ch.id, ch)
            print()

            await self.change_presence(activity=discord.Game("근무"))
            await message.channel.send(f"채널 [{message.guild.name}]이 추가되었습니다.")

        if message.content == '정지':
            await client.change_presence(activity=discord.Game("휴식"))

            # 일을 하고 있던 상황에서는 bool 값을 변경해야 함.
            if self.work:
                self.work = 0
                self.task.notice_stop()

                print(f"{message.guild.name}에서 [정지]를 입력\n")
                for ch in channels:
                    await ch.send(f"{message.guild.name}에서 [정지]를 입력하였습니다.")

TOKEN = os.environ.get('BOT_TOKEN')
client = MyClient()
client.run(TOKEN)
