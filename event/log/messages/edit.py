import discord
from discord.ext import commands
import time
from datetime import datetime
from system.DB import DB
import io



intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class message_edit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        # 수정된 메시지가 동일한 경우 무시
        if before.content == after.content:
            return

        채팅_메시지=self.bot.get_channel(int(1305859106275463178))
        print(f"메시지 수정 확인됨: {before.author.name}")
        await DB.execute_query(
            """
            INSERT INTO logs (event_type, user_id, user_name, description)
            VALUES (%s, %s, %s, %s)
            """,
            (
                "채팅",
                before.author.id,
                before.author.name,
                f"{before.author.name}({before.author.id}) 님이 메시지를 수정했습니다. "
                f"수정 전: {before.content}, 수정 후: {after.content} (채널: {before.channel.name})"
            )
        )
        # 수정 로그 텍스트 생성
        log_message = (
            f"{before.author.name}({before.author.id}) 님이 메시지를 수정했습니다.\n"
            f"**수정 전:** {before.content}\n"
            f"**수정 후:** {after.content}\n"
            f"**채널:** {before.channel.mention}\n"
        )

        # 메시지가 2000자를 초과하면 텍스트 파일로 저장 후 전송
        if len(log_message) > 2000:
            with io.StringIO() as txt_file:
                txt_file.write(log_message)
                txt_file.seek(0)
                await 채팅_메시지.send(
                    f"{before.author.name}({before.author.id}) 님의 수정 로그가 너무 길어 파일로 제공합니다:",
                    file=discord.File(txt_file, filename="edit_log.txt")
                )
        else:
            # 2000자 이하일 경우 채널에 메시지 전송
            await 채팅_메시지.send(log_message)