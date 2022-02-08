import discord, os, datetime, pytz
import parsing as tool
from discord.ext import tasks

where = ["백마 광장", "학사 공지", "일반 소식", "사업단 소식"]
KST = pytz.timezone("Asia/Seoul")

class MyClient(discord.Client):
    async def on_ready(self):
        self.info = [dict() for _ in range(4)]
        self.prev_date = "22.02.09"
        print("Login")

    @tasks.loop(minutes=2)
    async def notice(self, ch):
        print("keep crawl")
        date = str(datetime.datetime.now(KST).date()).replace("-", ".")[2:]

        if date != self.prev_date:
            self.info = [dict() for _ in range(4)]
            self.prev_date = date

        for i in range(4):
            # ret[0] has a value that how many posts are uploaded in today
            ret, cnt = tool.what_you_want(i, date), 0
            temp = discord.Embed(title=where[i], description=ret[0], color=0x62c1cc)

            print(ret)
            for j in range(1, len(ret)):
                title = ret[j][1]
                if title in self.info[i]:
                    continue

                cnt += 1
                self.info[i][title] = 1
                title = str(ret[j][0] + "    " + ret[j][1])
                temp.add_field(name=title, value=ret[j][-1], inline=False)

            if cnt:
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
