import parse_with_selenium
import discord
import datetime
from discord.ext import tasks

TOKEN = 'YOUR TOKEN'

class MyClient(discord.Client):
    tool = parse_with_selenium.Driver()

    async def on_ready(self):
        self.info = [dict() for _ in range(5)]
        self.prev_date = "22.02.09"
        print('Logged on as', self.user)

    def notice_stop(self):
        self.notice.cancel()
        print("STOP!!")

    @tasks.loop(minutes=3)
    async def notice(self, ch):
        try:
            await self.change_presence(activity=discord.Game("근무 "))
            where = ["백마 광장", "학사 공지", "일반 소식", "사업단 소식", "교외활동, 인턴, 취업"]

            date = str(datetime.datetime.now().date()).replace("-", ".")[2:]
            print(f"crawl : {datetime.datetime.now()}")

            if date != self.prev_date:
                self.info = [dict() for _ in range(5)]
                self.prev_date = date

            for i in range(5):
                # ret[0] has a value that how many posts are uploaded in today
                ret, cnt = self.tool.what_you_want(i, date), 0
                temp = discord.Embed(title=where[i], description=ret[0], color=0x62c1cc)

                for j in range(1, len(ret)):
                    title = ret[j][1]
                    if title in self.info[i]:
                        continue

                    cnt += 1
                    self.info[i][title] = 1
                    title = str(ret[j][0] + "    " + ret[j][1])
                    temp.add_field(name=title, value=ret[j][-1], inline=False)

                if cnt:
                    print(f"{where[i]} : {self.info[i]}")
                    await ch.channel.send("", embed=temp)
        except BaseException as e:
            print(f"error : {e}")
            self.notice_stop()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '공지':
            try : 
                await self.notice.start(message)
            except:
                await self.change_presence(activity=discord.Game("근무 stopped"))

        # if message.content == '정지':
        #     await self.change_presence(activity=discord.Game("휴식"))
        #     await self.notice.cancel(message)


client = MyClient()
client.run(TOKEN)
