from .phone.phone import phone

__all__ = ["setup"]  # setup 함수만 공개

def setup(bot):
    bot.add_cog(phone(bot))