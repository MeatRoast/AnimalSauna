# 라이브러리
import discord
from discord.ext import commands, tasks
from datetime import datetime
import atexit
from dotenv import dotenv_values
import asyncio
from system.DB import DB
from system.status import *

env_variables = dotenv_values("./system/private/.env")  # env파일에서 BOT TOKEN 가져옴
if "BOT_TOKEN" not in env_variables:
    print("Error: BOT_TOKEN is missing in .env file")
    exit(1)

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

# Commands Load
try:
    bot.load_extension("commands")
    bot.load_extension("event")
except Exception as e:
    print(f"Error loading extensions: {type(e).__name__} - {e}")

@bot.event
async def on_connect():
    print("Connecting to the Discord Server!")

@bot.event
async def on_ready():
    try:
        await setup_status(bot)
        await DB.connect()
        print("\n\n")
        print("             Copyright ©2021 MeatRoast Inc. All rights reserved")
        print(f"         BOT NAME: {bot.user.name}")
        print(f"         BOT Client ID: {bot.user.id}")
        print("\n------------------")
    except Exception as e:
        print(f"[{datetime.now()}] Login Error: {type(e).__name__} - {e}")

@bot.event
async def on_disconnect():
    print("Disconnected from Discord server! Waiting for automatic reconnection...")

# 봇 서비스 실행
def run_bot():
    global chat_log_file  # 전역 변수로 설정
    chat_log_file = open(f"./chatlog/{datetime.now().strftime('%Y-%m-%d')}.txt", "a", encoding="utf-8")
    atexit.register(chat_log_file.close)  # 스크립트 종료 시 파일 닫기
    bot.run(env_variables["BOT_TOKEN"])
