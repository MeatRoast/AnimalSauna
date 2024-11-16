# 각 명령어 불러오기
from .chatlog.chatlogs import chatlogs_event
from .log.join.join import join
def setup(bot):
    bot.add_cog(chatlogs_event(bot))
    bot.add_cog(join(bot))