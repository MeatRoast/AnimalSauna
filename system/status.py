import discord
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

status = cycle(
    [
        'Copyright ©2021-2024 MeatRoast. All rights reserve',
    ]
)

async def setup_status(bot):
    @tasks.loop(seconds=60)
    async def change_status():
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(
                next(status)
            )
        )
    change_status.start()

