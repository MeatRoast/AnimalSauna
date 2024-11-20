import discord
from discord.ext import commands
from discord.commands import Option
from system.DB import DB

class logs_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="로그조회")
    async def 서버로그(
        self,
        ctx: discord.ApplicationContext,
        # 로그: Option(str, "로그를 선택해주세요", choices=["ALL", "입퇴장", "초대", "채팅", "음성", "추방", "차단", "역할", "채널", "기타"]),
        로그: Option(str, "로그를 선택해주세요", choices=["ALL", "입퇴장","채팅"]),
        시작날짜: Option(str, "시작날짜를 입력해주세요. (ex: 2023-09-01)"),
        종료날짜: Option(str, "종료날짜를 입력해주세요. (ex: 2023-09-10)"),
        사용자: Option(discord.User, required=False),
    ):
        if 로그 == "ALL":
            if 사용자 is None:
                ALL_logs = await DB.execute_query(f"SELECT event_type, user_name, description, timestamp FROM logs WHERE date(timestamp) BETWEEN '{시작날짜}' AND '{종료날짜}';")
                await ctx.respond(f"```{ALL_logs}```")
            else:
                ALL_logs = await DB.execute_query(f"SELECT event_type, user_name, description, timestamp FROM logs WHERE user_id = {사용자.id} AND date(timestamp) BETWEEN '{시작날짜}' AND '{종료날짜}';")
                await ctx.respond(f"```{ALL_logs}```")

        if 로그 == "입퇴장":
            if 사용자 is None:
                join_logs = await DB.execute_query(f"SELECT event_type, user_name, description, timestamp FROM logs WHERE event_type = '입퇴장' AND date(timestamp) BETWEEN '{시작날짜}' AND '{종료날짜}';")
                await ctx.respond(f"```{join_logs}```")
            else:
                join_logs = await DB.execute_query(f"SELECT event_type, user_name, description, timestamp FROM logs WHERE event_type = '입퇴장' AND user_id = {사용자.id} AND date(timestamp) BETWEEN '{시작날짜}' AND '{종료날짜}';")
                await ctx.respond(f"```{join_logs}```")
                
        if 로그 == "채팅":
            if 사용자 is None:
                chat_logs = await DB.execute_query(f"SELECT event_type, user_name, description, timestamp FROM logs WHERE event_type = '입퇴장' AND date(timestamp) BETWEEN '{시작날짜}' AND '{종료날짜}';")
                await ctx.respond(f"```{chat_logs}```")
            else:
                chat_logs = await DB.execute_query(f"SELECT event_type, user_name, description, timestamp FROM logs WHERE event_type = '입퇴장' AND user_id = {사용자.id} AND date(timestamp) BETWEEN '{시작날짜}' AND '{종료날짜}';")
                await ctx.respond(f"```{chat_logs}```") 
