from .ad.ad_phone import ad_phone

__all__ = ["setup"]  # setup 함수만 공개

def setup(bot):
    bot.add_cog(ad_phone(bot))