# import
from Utils.data import *

# class
class Text(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# this endpoint is currently not ready

# setup
def setup(bot):
    bot.add_cog(Text(bot))
