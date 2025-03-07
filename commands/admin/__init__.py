#채팅관련 Admin Commands
from .chatlogs.chatlogs import chatlogs

#Role Admin Commands
from .roles.role import role

from .log.logs import logs_commands
__all__ = ["setup"]  # setup 함수만 공개

def setup(bot):
    bot.add_cog(chatlogs(bot))
    bot.add_cog(role(bot))
    bot.add_cog(logs_commands(bot))