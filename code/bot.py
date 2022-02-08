import discord, os, datetime
import parsing as tool
from discord.ext import tasks

where = ["백마 광장", "학사 공지", "일반 소식", "사업단 소식"]

class MyClient(discord.Client):
    async def on_ready(self):
        self.info = [dict()] * 4

    @tasks.loop(minutes=5)
    async def notice(self, ch):
        date = str(datetime.datetime.now().date()).replace("-", ".")[2:]
        prev_date = str(open("data_date.txt").readline())

        if date != prev_date:
            self.info = [dict()] * 4
            with open("../txtFile/data_date.txt", "w") as f:
                f.write(date)

        for i in range(4):
            # ret[0] has a value that how many posts are uploaded in today
            ret = tool.what_you_want(i, date)
            temp = discord.Embed(title=where[i], description=ret[0], color=0x62c1cc)

            for j in range(1, len(ret)):
                title = ret[j][1]
                if title in self.info[i]:
                    continue

                self.info[i][title] = 1
                title = str(ret[j][0] + "    " + ret[j][1])
                temp.add_field(name=title, value=ret[j][-1], inline=False)

            await ch.channel.send("", embed=temp)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '공지':
            await self.change_presence(activity=discord.Game("근무"))
            await self.notice.start(message)

TOKEN = os.environ.get('BOT_TOKEN')
client = MyClient()
client.run(TOKEN)