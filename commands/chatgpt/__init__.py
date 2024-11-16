from .chatgpt.chatgpt import chatgpt
from .reset.reset import chatgpt_reset

__all__ = ["setup"]  # setup 함수만 공개

def setup(bot):
    bot.add_cog(chatgpt(bot))
    bot.add_cog(chatgpt_reset(bot))