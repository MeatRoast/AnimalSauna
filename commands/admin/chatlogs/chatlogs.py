import discord
from discord.ext import commands
from discord.commands import Option
from system.DB import DB
intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class chatlogs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="서버 채팅로그를 다운로드 합니다")
    async def 채팅로그(self,ctx,날짜: Option(str,"날짜를 입력해주세요(ex)2023-09-01)")):
        파일명 = f'chatlog/{날짜}.txt'
        role_ids = [role.id for role in ctx.author.roles]
        print(role_ids)
        rows = await DB.execute_query("SELECT role_id FROM role WHERE role_id IN %s", (tuple(role_ids),))
        if rows:
            try:
                file = discord.File(파일명)
                await ctx.respond(f'{날짜}의 채팅 로그입니다:', file=file)
            except FileNotFoundError:
                await ctx.respond(f'{날짜}에 해당하는 채팅 로그 파일을 찾을 수 없습니다.\n2023년 9월 1일 경우 2023-09-01 입력')
        else:
            await ctx.respond(f"해당 유저는 접근 권한이 없습니다.")


    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="채팅창을 해당 갯수만큼 청소를 합니다.", administrator=True)
    async def 청소(
        self,
        ctx,
        개수: Option(str, "1 ~ 5000개의 메시지를 삭제할수 있습니다.")
    ):
        class Button(discord.ui.View):
            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red)
            async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                a = int(개수)+1
                await ctx.channel.purge(limit=a)
                await ctx.send(f"**<@!{interaction.user.id}>**님의 요청으로\n**{개수}**개의 내용을 삭제했습니다.")
            async def interaction_check(self, interaction: discord.Interaction):
                return interaction.user.id == ctx.author.id
            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
            async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                await ctx.send("취소되었습니다.")
            async def interaction_check(self, interaction: discord.Interaction):
                return interaction.user.id == ctx.author.id
        e = int(개수)+1
        if e <= 5001:  
            await ctx.respond(f"{개수}개의 내역을 삭제 하시나요?", view=Button())
        else:
            await ctx.respond("5000까지 내용만 삭제 가능합니다.")
    @청소.error
    async def _cls_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("삭제할 수를 입력해주세요.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("해당 명령어는 관리자만 사용 가능합니다.")