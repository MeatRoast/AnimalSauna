
import discord
from discord.ext import commands
from discord.commands import Option
from system.DB import DB


class voicerank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="보이스랭킹")
    async def 보이스랭킹(self, ctx):
        timetop = await ctx.respond("유저 데이터를 불러오고 있습니다.. 잠시만 기다려주세요!")
        time_rank_data = 0  # 시작 데이터 인덱스
        per_page = 10  # 페이지당 데이터 수
        def format_duration(duration):
            duration_hours = int(duration // 3600)
            duration_minutes = int((duration % 3600) // 60)
            duration_seconds = int(duration % 60)
            return f"{duration_hours}시간 {duration_minutes}분 {duration_seconds}초"
        rows = await DB.execute_query(f"SELECT id, time FROM users ORDER BY time DESC LIMIT {per_page} OFFSET {time_rank_data};")
        if rows:
            embed = discord.Embed(title="보이스 랭킹", color=0xF1B3FF)
            for index, row in enumerate(rows):
                member = await self.bot.fetch_user(int(row['id']))
                if member:
                    duration = row["time"]
                    duration_formatted = format_duration(duration)
                    embed.add_field(name=f"", value=f"**{index + 1}**. {member.mention}: **{duration_formatted}**", inline=False)
                    
            class timeRankButton(discord.ui.View):
                @discord.ui.button(label="다음", style=discord.ButtonStyle.primary)
                async def 다음(self, button: discord.ui.Button, interaction: discord.Interaction):
                    nonlocal time_rank_data
                    time_rank_data += per_page  # 다음 페이지의 시작 데이터 인덱스
                    await timetop.edit_original_response(content="데이터를 가져오고 있습니다. 잠시만 기다려주세요!", view=timeRankButton())
                    rows = await DB.execute_query(f"SELECT id, time FROM users ORDER BY time DESC LIMIT {per_page} OFFSET {time_rank_data};")
                    if rows:
                        embed = discord.Embed(title="보이스 랭킹", color=0xF1B3FF)
                        for index, row in enumerate(rows):
                            member = await ctx.bot.fetch_user(int(row['id']))
                            if member:
                                duration = row["time"]
                                duration_formatted = format_duration(duration)
                                embed.add_field(name="", value=f"**{time_rank_data + index + 1}**. {member.mention}:  **{duration_formatted}**", inline=False)
                        await timetop.edit_original_response(content=" ", embed=embed, view=timeRankButton())
                    else:
                        await timetop.edit_original_response(content="보이스 랭킹 정보가 없습니다.")
                async def interaction_check(self, interaction: discord.Interaction):
                    return interaction.user.id == ctx.author.id
    
            await timetop.edit_original_response(content=" ", embed=embed, view=timeRankButton())
        else:
            await timetop.edit_original_response(content="보이스 랭킹 정보가 없습니다.")
