import discord
from discord.ext import commands
import json
from system.DB import DB # DB 연동

class chatgpt_reset(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(description="ChatGPT 대화 기록을 초기화합니다.")
    async def chatgpt리셋(self, ctx):
        user_id = str(ctx.author.id)  # Discord 사용자 ID

        # 초기화된 기록
        initial_conversation = [{"role": "system", "content": "You are a helpful assistant."}]

        try:
            # MySQL에 초기화된 기록 저장
            await DB.execute_update(
                """
                INSERT INTO conversations (user_id, history)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE history = %s
                """,
                (user_id, json.dumps(initial_conversation), json.dumps(initial_conversation))
            )
            await ctx.respond("대화 기록이 초기화되었습니다.")
        except Exception as e:
            print(f"DB 초기화 오류: {e}")
            await ctx.respond("대화 기록 초기화 중 오류가 발생했습니다.")