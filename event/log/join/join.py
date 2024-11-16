import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class join(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f"신규유저 확인됨: {member.name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f"유저 나감: {member.name}")