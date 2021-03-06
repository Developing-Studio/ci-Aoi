import random

import aoi
from discord.ext import commands


class ServerGambling(commands.Cog):
    def __init__(self, bot: aoi.AoiBot):
        self.bot = bot

    @property
    def description(self):
        return "Gambling and games :)"

    @commands.command(
        brief="Rolls dice. Number of dice and sides are optional; number must be supplied if number of sides is."
    )
    async def roll(self, ctx: aoi.AoiContext, num: int = 5, sides: int = 6):
        if num <= 0 or num > 50:
            return await ctx.send_error("Number of dice must be from 1 to 50")
        if sides < 6 or sides > 100:
            return await ctx.send_error("Number of sides must be between 6 and 100")
        counted = {}
        dice = []
        for _ in range(num):
            die = random.randint(1, sides + 1)
            counted[die] = counted.get(die, 0) + 1
            dice.append(die)
        await ctx.send_info(
            f"**Average:** {round(sum(dice) / len(dice), 1):0.1f} - "
            f"**Total:** {sum(dice)} - "
            f"**Number Rolled:** {len(dice)}\n" +
            "-".join(map(str, dice)) + "\n"
        )

    @commands.command(
        brief="Flip a coin, with an optional bet",
        aliases=["cf"]
    )
    async def coinflip(self, ctx: aoi.AoiContext, bet: int = 0, h_or_t: str = "h"):
        ht = random.choice(["heads", "tails"])
        if not bet:
            return await ctx.send_info(f"You got **{ht}**")
        if h_or_t.lower() not in "heads tails h t".split(" "):
            return await ctx.send_error("Must specify heads or tails")
        if bet > await self.bot.db.get_guild_currency(ctx.author):
            return await ctx.send_error("You don't have enough currency.")
        if bet < 5:
            return await ctx.send_error("You must bet at least 5.")
        await ctx.send_info(f"You got **{ht}**. You {'win' if ht[0] == h_or_t.lower()[0] else 'lose'} ${bet:,}")
        await self.bot.db.award_guild_currency(ctx.author, bet if ht[0] == h_or_t.lower()[0] else -bet)

    @commands.command(
        brief="100 - 10x bet, >90 - x4 bet, >66 - x2 bet",
        aliases=["br"]
    )
    async def betroll(self, ctx: aoi.AoiContext, bet: int):
        if bet > await self.bot.db.get_guild_currency(ctx.author):
            return await ctx.send_error("You don't have enough currency.")
        if bet < 5:
            return await ctx.send_error("You must bet at least 5.")
        r = random.randint(0, 101)
        if r == 100:
            win = bet * 10
        elif r > 90:
            win = bet * 4
        elif r > 66:
            win = bet * 2
        else:
            win = 0
        await ctx.send_info(f"You got a {r}. {'Better luck next time?' if not win else 'You won ' + str(win) + '!'}")
        await self.bot.db.award_guild_currency(ctx.author, win - bet)


def setup(bot: aoi.AoiBot) -> None:
    bot.add_cog(ServerGambling(bot))
