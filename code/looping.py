import discord, datetime, parsing as tool, pytz, asyncio
from discord.ext import tasks, commands

def status():
    print(f"now running {asyncio.get_running_loop()}")

class MyCog(commands.Cog):
    def __init__(self):
        self.channels = dict()
        self.info = [dict() for _ in range(4)]
        self.prev_date = "22.02.09"
        await self.crawl()

    @tasks.loop(minutes=2)
    async def crawl(self):
        self.task = asyncio.create_task(self.notice())

    async def notice(self):
        for ch in self.channels:
            print(f"연결된 채널 {ch.guild, ch.id}")

        where = ["백마 광장", "학사 공지", "일반 소식", "사업단 소식"]

        KST = pytz.timezone("Asia/Seoul")
        withtime = str(datetime.datetime.now(KST)).replace("-", ".")[2:].split()
        date = withtime[0]
        time = withtime[1].split(".")[0]
        print(f"date in korea : {date}, time in korea : {time}")

        if date != self.prev_date:
            self.info = [dict() for _ in range(4)]
            self.prev_date = date

        uploaded = []
        for i in range(4):
            # ret[0] has a value that how many posts are uploaded in today
            ret, cnt = tool.what_you_want(i, date), 0
            temp = discord.Embed(title=where[i], description=ret[0], color=0x62c1cc)

            uploaded.append(str(ret[0]).strip())
            for j in range(1, len(ret)):
                title = ret[j][1]
                if title in self.info[i]:
                    continue

                cnt += 1
                self.info[i][title] = 1
                title = str(ret[j][0] + "    " + ret[j][1])
                temp.add_field(name=title, value=ret[j][-1], inline=False)

            if cnt:
                for ch in self.channels:
                    print(f"send to : {ch.guild, ch.id}")
                    await ch.send("", embed=temp)

        print(f"Update : {uploaded}")
