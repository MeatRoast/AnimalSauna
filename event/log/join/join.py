import discord
from discord.ext import commands
from system.DB import DB

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class join(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f"신규유저 확인됨: {member.name}")
        # MySQL에 로그 저장
        await DB.execute_query("INSERT INTO logs (event_type, user_id, user_name, description)VALUES (%s, %s, %s, %s)",
            ("입퇴장", member.id, member.name, f"{member.name}({member.id}) 님이 서버에 입장했습니다.")
        )
        입장=self.bot.get_channel(int(1305859037715497011))
        await 입장.send(f"{member.name}({member.id}) 님이 서버에 입장했습니다")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f"유저 나감: {member.name}")
        # MySQL에 로그 저장
        await DB.execute_query("INSERT INTO logs (event_type, user_id, user_name, description)VALUES (%s, %s, %s, %s)",
            ("입퇴장", member.id, member.name, f"{member.name}({member.id}) 님이 서버에서 퇴장했습니다.")
        )
        퇴장=self.bot.get_channel(int(1305859062830993459))
        await 퇴장.send(f"{member.name}({member.id}) 님이 서버에 퇴장했습니다")
