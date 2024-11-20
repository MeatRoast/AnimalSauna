import discord
from discord.ext import commands
import time
from datetime import datetime
from system.DB import DB
import io

class message_delete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        # 봇이 보낸 메시지는 무시
        if message.author.bot:
            return
        
        채팅_메시지=self.bot.get_channel(int(1305859106275463178))

        print(f"메시지 삭제 확인됨: {message.author.name}")

        # 삭제 로그 텍스트 생성
        log_message = (
            f"{message.author.name}({message.author.id}) 님의 메시지가 삭제되었습니다.\n"
            f"**삭제된 메시지:** {message.content}\n"
            f"**채널:** {message.channel.mention}\n"
        )
        await DB.execute_query(
            """
            INSERT INTO logs (event_type, user_id, user_name, description)
            VALUES (%s, %s, %s, %s)
            """,
            (
                "채팅",
                message.author.id,
                message.author.name,
                f"{message.author.name}({message.author.id}) 님이 메시지를 삭제했습니다. "
                f"채널: {message.channel.name})\n삭제된 메시지: {message.content}"
            )
        )
        # 메시지가 2000자를 초과하면 텍스트 파일로 저장 후 전송
        if len(log_message) > 2000:
            with io.StringIO() as txt_file:
                txt_file.write(log_message)
                txt_file.seek(0)
                await 채팅_메시지.send(
                    f"{message.author.name}({message.author.id}) 님의 삭제 로그가 너무 길어 파일로 제공합니다:",
                    file=discord.File(txt_file, filename="delete_log.txt")
                )
        else:
            # 2000자 이하일 경우 채널에 메시지 전송
            await 채팅_메시지.send(log_message)
