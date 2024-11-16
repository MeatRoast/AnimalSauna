import discord
from discord.ext import commands
import time
from datetime import datetime

from .logs_save import *

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class chatlogs_event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_log_file = None
        self.current_date = None

    # 채팅로그 기록
    @commands.Cog.listener()
    async def on_message(self, message):  # self 추가
        if message.author.bot:
            return
        
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

        # 채팅 내용 로그 파일에 저장
        if date != self.current_date:
            if self.chat_log_file is not None:
                self.chat_log_file.close()

            self.chat_log_file = open(f"chatlog/{date}.txt", "a", encoding="utf-8")
            self.current_date = date

        print(f"[INFO][{st}][{message.channel.name}][{message.author}({message.author.id})] >> {message.content}")

        if self.chat_log_file:
            log_message = f"[INFO][{st}][{message.channel.name}][{message.author}({message.author.id})] >> {message.content}\n"
            self.chat_log_file.write(log_message)
            self.chat_log_file.flush()

        # 사진 및 첨부 파일 저장
        if message.attachments:
            await save_attachments(message.attachments, message.author.id, message)

        await self.bot.process_commands(message)  # self.bot으로 변경
