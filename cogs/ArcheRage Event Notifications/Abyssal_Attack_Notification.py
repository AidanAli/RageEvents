import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_pings
from main import allow_ping_role


class _AbyssalAttack(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        first_Abyssal = AndTrigger([CronTrigger(hour=15, minute=43, day_of_week='tue,thu,sat',
                                              timezone=pytz.timezone('US/Eastern'))])
        second_Abyssal= AndTrigger([CronTrigger(hour=20, minute=13, day_of_week='tue,thu,sat',
                                               timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, first_Abyssal)
        self.scheduler.add_job(self.send_message, second_Abyssal)

    async def send_message(self):
        channel = self.client.get_channel(event_pings)  # replace with your channel ID
        embed = Embed(title="Abyssal Attack", description="**Spawns in 15 Minutes**", color=0xff0000)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1055620637592395857/1105317992260178000/image.png")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send(f"<@&{allow_ping_role}>",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("_AbyssalAttack Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(_AbyssalAttack(client))
