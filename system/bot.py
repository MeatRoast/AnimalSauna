# 라이브러리
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import atexit
from dotenv import dotenv_values

#Bot File
from system.DB import DB
from system.status import *

env_variables = dotenv_values("./system/private/.env") # env파일 봇 TOKEN을 가져옴
intents = discord.Intents.all()
bot = commands.Bot(intents=intents)


bot.load_extension("commands") # 커멘드 정보 가져옴

@bot.event
async def on_ready():
    await setup_status(bot)
    # await DB.connect()
    print('')
    print('')
    print("             Copyright ©2021 MeatRoast Inc. All rights reserve")
    print("             ")
    print('')
    print("         BOT NAME:", bot.user.name)
    print("         BOT Clint ID:", bot.user.id)
    print('')
    print("------------------")

#봇 서비스 실행
def run_bot():
    global chat_log_file  # 전역 변수로 설정
    chat_log_file = open(f"./chatlog/{datetime.now().strftime('%Y-%m-%d')}.txt", "a", encoding="utf-8")
    atexit.register(chat_log_file.close)  # 스크립트 종료 시 파일 닫기
    bot.run(env_variables["BOT_TOKEN"])