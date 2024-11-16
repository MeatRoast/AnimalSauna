import aiomysql
from dotenv import dotenv_values

env_variables = dotenv_values("./system/private/.env") # env파일 봇 TOKEN을 가져옴

class DB:
    def __init__(self):
        self.host = f'{env_variables["DB_IP"]}'
        self.port = 3306
        self.user = f'{env_variables["DB_USER"]}'
        self.password = f'{env_variables["DB_PASSWORD"]}'
        self.database = 'atten'
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True,  # 자동 커밋 설정
            maxsize=5
        )

    async def execute_query(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                rows = await cursor.fetchall()
                return rows

    async def execute_update(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                await conn.commit()

    async def execute_insert(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                await conn.commit()

# 인스턴스 생성
DB = DB()
