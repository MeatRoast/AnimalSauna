
import discord
from discord.ext import commands
from discord.commands import Option
import json
from system.DB import DB # DB 연동
import openai
from dotenv import dotenv_values

env_variables = dotenv_values("./system/private/.env") # env파일 봇 TOKEN을 가져옴
class chatgpt(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(description="Chat GPT 테스트")
    async def chatgpt(self, ctx, 질문: Option(str, "질문을 입력해주세요")):
        user_id = str(ctx.author.id)  # Discord 사용자 ID

        # MySQL에서 대화 기록 불러오기
        try:
            records = await DB.execute_query(
                "SELECT history FROM conversations WHERE user_id = %s", (user_id,)
            )
            if records:
                # 기존 대화 기록이 있으면 JSON으로 로드
                conversation = json.loads(records[0]["history"])
            else:
                # 대화 기록이 없으면 초기화
                conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        except Exception as e:
            print(f"DB 불러오기 오류: {e}")
            await ctx.respond("데이터베이스에서 대화 기록을 불러오는 중 오류가 발생했습니다.")
            return

        # 새로운 질문 추가
        conversation.append({"role": "user", "content": f"{질문}"})

        # 초기 응답
        chatgptwait = await ctx.respond("응답을 기다리고 있습니다...")
        openai.api_key = env_variables["CHATGPT_KEY"]

        try:
            # OpenAI API 호출
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            # ChatGPT의 응답 추가
            chatgpt = response['choices'][0]['message']['content']
            conversation.append({"role": "assistant", "content": chatgpt})

            # 대화 기록을 MySQL에 저장
            try:
                await DB.execute_update(
                    """
                    INSERT INTO conversations (user_id, history)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE history = %s
                    """,
                    (user_id, json.dumps(conversation), json.dumps(conversation))
                )
            except Exception as e:
                print(f"DB 저장 오류: {e}")
                await chatgptwait.edit_original_response(content="대화 기록 저장 중 오류가 발생했습니다.")

            # 결과 출력
            print(chatgpt)
            await chatgptwait.edit_original_response(content=f"{chatgpt}")

        except Exception as e:
            # 에러 처리
            print(f"ChatGPT API 호출 오류: {e}")
            await chatgptwait.edit_original_response(content="ChatGPT 호출 중 오류가 발생했습니다. 다시 시도해주세요.")