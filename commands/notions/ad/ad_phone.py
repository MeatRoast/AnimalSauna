import discord
from discord.ext import commands
import aiohttp  # 비동기 HTTP 요청을 위해 aiohttp 사용
import time
import hmac
import hashlib
import random
from system.DB import DB
from dotenv import dotenv_values
# 보안상 위배될수 있는 부분은 제외 되었습니다
env_variables = dotenv_values("./system/private/.env") # env파일 봇 TOKEN을 가져옴
# API KEY와 API SECRET 설정
API_KEY = f'{env_variables["PA_API_KEY"]}'
API_SECRET = f'{env_variables["PA_API_SE"]}'
from_number = f'{env_variables["PA_API_NUMBER"]}'

# 봇 인텐트 및 설정
intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

class AdModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="광고 문자 보내기")

        # 제목 필드
        self.add_item(discord.ui.InputText(label="제목", placeholder="광고 문자의 제목을 입력하세요"))
        # 내용 필드
        self.add_item(discord.ui.InputText(label="내용", style=discord.InputTextStyle.long, placeholder="광고 문자의 내용을 입력하세요"))

    async def callback(self, interaction: discord.Interaction):
        title = self.children[0].value  # 제목
        content = self.children[1].value  # 내용

        # 사용자가 입력한 제목과 내용을 확인할 수 있는 임베드 생성
        embed = discord.Embed(
            title="광고 문자 미리보기",
            description="아래 내용을 확인 후 '보내기'를 누르면 광고 문자가 발송됩니다.",
            color=discord.Color.blue()
        )
        embed.add_field(name="제목", value=title, inline=False)
        embed.add_field(name="내용", value=content, inline=False)

        # 보내기 및 취소 버튼이 있는 View 생성
        view = ConfirmView(title, content)
        await interaction.response.send_message(embed=embed, view=view)


class ConfirmView(discord.ui.View):
    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content

    def generate_signature(self, api_key, api_secret, now, salt):
        secret_key = bytes(api_secret, 'utf-8')
        message = f'{now}{salt}'.encode('utf-8')
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        return signature

    @discord.ui.button(label="보내기", style=discord.ButtonStyle.green)
    async def send_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # 보안상 위배될수 있는 부분은 제외 되었습니다
        if users:
            ad_phone_users = len(users)  # 광고 메시지 대상자 수
            for user in users:
                # 보안상 위배될수 있는 부분은 제외 되었습니다
                now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                salt = ''.join(random.choice('0123456789ABCDEF') for i in range(64))  # 64자리의 랜덤 값 생성
                signature = self.generate_signature(API_KEY, API_SECRET, now, salt)
                url = "https://api.coolsms.co.kr/messages/v4/send"

                headers = {
                    'Authorization': f'HMAC-SHA256 apiKey={API_KEY}, date={now}, salt={salt}, signature={signature}',
                    'Content-Type': 'application/json',
                }

                # 비동기 HTTP 요청 처리
                async with aiohttp.ClientSession() as session:
                    data = {
                        'message': {
                            'to': phone_number,
                            'from': from_number,
                            'subject': f'{self.title}',
                            'text': f'(광고)\n{self.content}\n\n무료수신거부: 080-600-5653',
                            'type': 'LMS'  # 광고 문자 발송을 위해 LMS 설정
                        }
                    }

                    try:
                        async with session.post(url, json=data, headers=headers) as response:
                            if response.status == 200:
                                res_json = await response.json()
                                print(f"API Request: {interaction.user} {res_json}")
                            else:
                                print(f"인증 문자 전송에 실패했습니다: {response.status}")
                    except Exception as e:
                        print(f"HTTP 요청 중 오류 발생: {str(e)}")

            # 성공 메시지 전송
            embed2 = discord.Embed(
                title="광고문자를 전송했습니다",
                description=f"총 {ad_phone_users}명에게 전송되었습니다.",
                color=0xabcee9
            )
            await interaction.response.edit_message(embed=embed2, view=None)

        else:
            await interaction.response.send_message("광고 문자를 보낼 대상이 없습니다.")

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def cancel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content="광고 문자 전송이 취소되었습니다.", embed=None, view=None)

class ad_phone(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    phone_command = discord.SlashCommandGroup("광고문자", "광고문자보내기")

    # 명령어: 모달 표시
    @phone_command.command(description="광고 문자를 보낼 정보를 입력합니다")
    async def 보내기(self, ctx: discord.ApplicationContext):
        modal = AdModal()
        await ctx.send_modal(modal)