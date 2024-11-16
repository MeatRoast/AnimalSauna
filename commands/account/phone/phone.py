import discord
from discord.ext import commands
from discord import Option
import re
import requests
import time
import hmac
import hashlib
import base64
import random
import asyncio  # 비동기 대기를 위해 추가
from system.DB import DB
from dotenv import dotenv_values

env_variables = dotenv_values("./system/private/.env") # env파일 봇 TOKEN을 가져옴
# API KEY와 API SECRET 설정
API_KEY = f'{env_variables["PA_API_KEY"]}'
API_SECRET = f'{env_variables["PA_API_SE"]}'
from_number = f'{env_variables["PA_API_NUMBER"]}'

# 봇 인텐트 및 설정
intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class phone(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldown_users = {}  # 쿨다운을 저장할 딕셔너리

    # 서명 생성 함수
    def generate_signature(self, api_key, api_secret, now, salt):
        secret_key = bytes(api_secret, 'utf-8')
        message = f'{now}{salt}'.encode('utf-8')
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        return signature

    # 랜덤 코드값 생성
    def generate_verification_code(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    phone_command = discord.SlashCommandGroup("본인인증", "본인 인증 서비스 관련 명령어")

    # 쿨다운 체크 함수
    async def is_in_cooldown(self, user_id):
        if user_id in self.cooldown_users:
            remaining_time = self.cooldown_users[user_id] - time.time()
            if remaining_time > 0:
                return remaining_time
        return None

    # 본인인증 명령어
    @phone_command.command(description="휴대폰 본인인증을 합니다")
    async def 전송(self, ctx, 번호: Option(str, "고객님의 휴대폰 번호를 입력해주세요")):
        user_id = ctx.author.id

        # 쿨다운 체크
        cooldown_remaining = await self.is_in_cooldown(user_id)
        if cooldown_remaining:
            await ctx.respond(f"재 인증 요청은 **{int(cooldown_remaining)}**초 후 다시 시도해주세요.", ephemeral=True)
            return

        phone12 = await DB.execute_query("select * from users where id = %s", (user_id,))
        if phone12:
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            salt = ''.join(random.choice('0123456789ABCDEF') for i in range(64))  # 64자리의 랜덤 값 생성
            signature = self.generate_signature(API_KEY, API_SECRET, now, salt)

            # 임의로 생성된 6자리 인증 코드
            verification_code = self.generate_verification_code()

            # CoolSMS API 요청
            url = "https://api.coolsms.co.kr/messages/v4/send"
            headers = {
                'Authorization': f'HMAC-SHA256 apiKey={API_KEY}, date={now}, salt={salt}, signature={signature}',
                'Content-Type': 'application/json',
            }
            data = {
                'message': {  # 단일 메시지로 수정
                    'to': 번호,  # 수신자의 전화번호
                    'from': from_number,  # 발신자 전화번호 (쿨에스엠에스에 등록된 발신번호)
                    'text': f'고객님께서 요청하신 인증번호는 [ {verification_code} ] 입니다.\n\n[ Discord 밤의 새벽 서버 ]',
                }
            }
            try:
                response = requests.post(url, json=data, headers=headers)
                print(response)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                print(f"API Request: {ctx.author}({user_id}) {response.json()}")
                # 보안상 위배될수 있는 부분은 제외 되었습니다
                # 인증 성공 시 응답 처리
                embed = discord.Embed(
                    title="요청하신 휴대폰 번호로 인증문자를 전송했습니다.",
                    description=f"**{번호}** 번호로 요청했습니다. [/본인인증 인증 인증번호]를 입력해주세요\n 유효시간은 5분 입니다.",
                    color=0xabcee9
                )
                await ctx.respond(embed=embed, ephemeral=True)
                embed2 = discord.Embed(
                    title="요청하신 휴대폰 번호로 인증문자를 전송했습니다.",
                    description=f"[/본인인증 인증 인증번호]를 입력해주세요\n 유효시간은 5분 입니다.",
                    color=0xabcee9
                )
                await ctx.respond(f"{ctx.author.mention}",embed=embed2)
                # 쿨다운 설정 (5분 동안 해당 유저는 다시 요청 불가)
                self.cooldown_users[user_id] = time.time() + 300  # 현재 시간에 300초를 더한 값을 저장

                # 5분 후 인증 번호 초기화 (비동기 처리)
                await asyncio.sleep(300)

                # 보안상 위배될수 있는 부분은 제외 되었습니다

            except requests.exceptions.HTTPError as err:
                await ctx.send(f"인증 문자 전송에 실패했습니다: {err}", ephemeral=True)
                if response is not None:
                    print(f"API Request: {ctx.author}({user_id}) {response.json()}")
        else:
            await ctx.respond("해당 고객님은 서비스에 미가입 상태입니다.\n[ /약관 이용약관 ] 먼저 진행후 진행해주세요.", ephemeral=True)

    @phone_command.command(description="본인인증 번호를 입력합니다.")
    async def 인증(
        self,
        ctx,
        인증: Option(int, "인증번호를 입력해주세요")
    ):
        user_id = ctx.author.id
        if not 인증:
            await ctx.respond("문자 인증번호를 입력해주세요.")
        else:
            # 보안상 위배될수 있는 부분은 제외 되었습니다
            if phone_num:
                phone_var = phone_num[0]['phone_num']
                if phone_var == 인증:
                    await ctx.respond("고객님 본인인증이 완료되었습니다.")
                    # 보안상 위배될수 있는 부분은 제외 되었습니다
                elif phone_var is None:
                    await ctx.respond("인증번호를 먼저 발급해주세요.")
                else:
                    await ctx.respond("인증번호가 일치하지 않습니다.")
            else:
                await ctx.respond("인증번호가 일치하지 않습니다.")
