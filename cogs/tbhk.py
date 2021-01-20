import discord
from discord.ext import commands
import aoi


class TBHK(commands.Cog):
    def __init__(self, bot: aoi.AoiBot):
        self.bot = bot

    @property
    def description(self) -> str:
        return "TBHK things, cuz Aoi"


def setup(bot: aoi.AoiBot) -> None:
    bot.add_cog(TBHK(bot))
