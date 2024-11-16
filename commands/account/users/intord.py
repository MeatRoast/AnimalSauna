import discord
from discord.ext import commands
from discord.commands import Option
import json
from system.DB import DB # DB 연동
import openai
from dotenv import dotenv_values

env_variables = dotenv_values("./system/private/.env") # env파일 봇 TOKEN을 가져옴
class intod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @discord.slash_command(description="자기소개")
    async def 자기소개(
        self,
        ctx,
        닉네임: Option(str, "닉네임을 입력해주세요."),
        나이: Option(str,"태어난 년도를 선택해주세요", choices=["2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998"]),
        성별: Option(str,"성별을 선택해주세요", choices=["여자","남자"]),
        경로: Option(str, "입장경로를 입력해주세요."),
    ):
        embed=(
            discord.Embed(
                title=f"자기소개 정보 입니다.",
                description="제공한 정보가 전부 사실이며 제공한 개인정보가 거짓일 경우 약관에 의해 제재 될수 있다는 점을 동의합니다.",
                color=0xFBFF6C
            )
            .add_field(
                name=f"{닉네임}",
                value="닉네임",
                inline=False
            )
            .add_field(
                name=f"{나이}년",
                value="생년(나이)",
                inline=False
            )
            .add_field(
                name=f"{성별}",
                value="성별",
                inline=False
            )
            .add_field(
                name=f"{경로}",
                value="경로",
                inline=False
            )
        )
        #await DB.execute_insert("INSERT IGNORE INTO users (id, nickname, chat, time, phone, age, gender, phone_num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(ctx.author.id, 닉네임, 0, 0, None, 나이, 성별, None))
        await DB.execute_query("UPDATE users SET nickname=%s, age=%s, gender=%s WHERE id=%s", (닉네임, 나이, 성별, ctx.author.id))
        괄챗전송 = self.bot.get_channel(int(1305909956163145738))
        await 괄챗전송.send(f"{ctx.author.mention}({ctx.author.id})",embed=embed)
        await ctx.respond(embed=embed)
    
    users1 = discord.SlashCommandGroup("유저", "유저 관리 명령어")
    @commands.has_permissions(administrator=True)
    @users1.command(description="서버에 등록된 유저 명단을 불러옵니다")
    async def 리스트(self, ctx):
        # 데이터베이스에서 유저 정보를 가져옵니다.
        data = await DB.execute_query("select * from users")
        
        # 데이터를 JSON 형식으로 변환
        json_data = [dict(row) for row in data]  # row를 dict로 변환
        file_name = "user_list.json"
        
        # JSON 파일로 저장
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)

        # Discord에 JSON 파일 업로드
        await ctx.respond("유저 명단입니다:", file=discord.File(file_name))

    @commands.has_permissions(administrator=True)
    @users1.command(description="서버에 등록된 유저 정보를 강제 삭제 합니다")
    async def 삭제(self,ctx,유저: Option(str, "유저고유아이디를 입력해주세요")):
        pass
        await ctx.respond("삭제")

    @commands.has_permissions(administrator=True)
    @users1.command(description="서버에 등록된 유저 정보를 강제 삭제 합니다")
    async def 강제가입(self,
        ctx,
        유저: Option(str, "유저고유아이디를 입력해주세요"),
        닉네임: Option(str, "닉네임을 입력해주세요."),
        나이: Option(str,"태어난 년도를 선택해주세요", choices=["2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","1997","1996 이상"]),
        성별: Option(str,"성별을 선택해주세요", choices=["여자","남자"]),
        경로: Option(str, "입장경로를 입력해주세요."),
    ):
        pass
        await DB.execute_insert("INSERT IGNORE INTO users (id, nickname, chat, time, phone, age, gender, phone_num,tos3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(유저, 닉네임, 0, 0, None, 나이, 성별, None,"Y"))
        await ctx.respond(f"해당정보로 강제가입이 완료되었습니다\n<@!{유저}>({유저}) / {닉네임} / {나이} / {성별} / {경로}")
    
