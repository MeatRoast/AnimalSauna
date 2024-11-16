import time
import aiohttp
import aiofiles
from datetime import datetime
import random
import string
import os

async def save_file(url, file_path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(file_path, "wb") as file:
                        await file.write(await response.read())
                    print(f"[INFO] 파일이 성공적으로 저장되었습니다: {file_path}")
                else:
                    print(f"[ERROR] 파일 다운로드 실패: {url} (상태 코드: {response.status})")
    except Exception as e:
        print(f"[ERROR] 파일 저장 중 오류 발생: {e}")

# 첨부 파일 저장 함수
async def save_attachments(attachments, user_id, message):
    attachment_dir = os.path.join("attachments", str(user_id), str(message.channel.id))
    os.makedirs(attachment_dir, exist_ok=True)
    for attachment in attachments:
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        file_extension = os.path.splitext(attachment.filename)[1]
        remd = await generate_random_code()  # await 추가
        file_name = f"{user_id}_file_{st}_{remd}{file_extension}"  # 파일명 생성
        file_path = os.path.join(attachment_dir, file_name)  # 파일 경로 생성


        await save_file(attachment.url, file_path)

        print(f"[INFO][{st}][{message.channel.name}][{message.author}({message.author.id})] >> 파일업로드 확인됨, 파일을 {file_name}에 저장함")

async def generate_random_code():
    letters = string.ascii_uppercase
    random_letter = ''.join(random.choice(letters) for _ in range(2))
    random_letter2 = ''.join(random.choice(letters) for _ in range(2))
    random_number = random.randint(1, 10000)
    random_number2 = random.randint(1, 10000)
    return f"{random_letter}{random_number}{random_letter2}{random_number2}"
