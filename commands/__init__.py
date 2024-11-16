# 각 명령어 불러오기
from .account import *
from .notions import *
from .admin import *
from .chatgpt import *
from .rank import *


__all__ = ["setup"]  # setup 함수만 공개

def setup(bot):
    account.setup(bot)
    notions.setup(bot)
    admin.setup(bot)
    chatgpt.setup(bot)
    rank.setup(bot)