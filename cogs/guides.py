import aoi
from discord.ext import commands


class Guides(commands.Cog):
    def __init__(self, bot: aoi.AoiBot):
        self.bot = bot

    @property
    def description(self):
        return f"Guides on how to use {self.bot.user.name if self.bot.user else ''}"

    @commands.command(brief="Shows the permission guide")
    async def permguide(self, ctx: aoi.AoiContext):
        await ctx.send_info(f"\n"
                            f"{self.bot.user.name if self.bot.user else ''}'s permissions are based off of a permission chain that "
                            f"anyone can view with `{ctx.prefix}lp`. The chain is evaluated "
                            f"from 0 to the top. The permission chain can be modified by anyone with "
                            f"administrator permission in a server. `{ctx.prefix}cmds permissions` can "
                            f"be used to view view a list of the permission commands\n"
                            f"The chain can be reset to the default with {ctx.prefix}rp"
                            )

    @commands.command(
        brief="Shows the currency guide"
    )
    async def currencyguide(self, ctx: aoi.AoiContext):
        await ctx.send_info(f"\n"
                            f"There are two types of currency in {self.bot.user.name if self.bot.user else ''}: "
                            f"Server and Global.\nGlobal currency is gained at the rate of $3/message, and can only "
                            f"be gained once every 3 minutes. Global currency is used over in "
                            f"`{ctx.prefix}cmds globalshop` to "
                            f"buy a title for your card an over in `{ctx.prefix}profilecard` to buy a background change "
                            f"for your profile card.\n"
                            f"Server currency is gained at a rate set by the server staff, and is viewable with "
                            f"`{ctx.prefix}configs`. It is used for roles and gambling - see `{ctx.prefix}cmds ServerShop` "
                            f"and `{ctx.prefix}cmds ServerGambling`."
                            )


def setup(bot: aoi.AoiBot) -> None:
    bot.add_cog(Guides(bot))
