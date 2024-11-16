import discord
from discord.ext import commands
from discord.commands import Option

from system.DB import DB

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class role(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    role = discord.SlashCommandGroup("역할", "역할 관리 명령어")
    @role.command(description="해당 역할의 실적 카운터를 추가 합니다.")
    async def 추가(self,ctx,role:discord.Role):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("해당 명령어는 서버 관리자만 사용 가능합니다.\n")
            return
        role_id = role.id
        rows = await DB.execute_query("select * from role where role_id = %s",(role_id))
        if rows:
            await ctx.respond(f"<@&{role_id}>는 실적 카운터 대상 역할 입니다.")
        else:
            await DB.execute_insert("INSERT IGNORE INTO role (role_id) values (%s)",(role_id))
            await ctx.respond(f"<@&{role_id}>에게 실적 역할에 추가 했습니다.")

    @role.command(description="해당 역할의 실적 카운터를 삭제 합니다,")
    async def 삭제(self,ctx,role:discord.Role):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("해당 명령어는 서버 관리자만 사용 가능합니다.\n")
            return
        role_id = role.id
        rows = await DB.execute_query("select * from role where role_id = %s",(role_id))
        if rows:
            await DB.execute_update("delete from role where role_id = %s",(role_id))
            await ctx.respond(f"<@&{role_id}>의 카운터 역할 삭제했습니다")
        else:
            await ctx.respond(f"<@&{role_id}>의 카운터 역할이 없습니다.")