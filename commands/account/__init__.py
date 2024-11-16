from .phone.phone import phone
from .users.intord import intod

__all__ = ["setup"]  # setup 함수만 공개

def setup(bot):
    bot.add_cog(phone(bot))
    bot.add_cog(intod(bot))