import inspect

import discord
from discord.ext import commands

import aoi


async def _can_run(_c: commands.Command, ctx: aoi.AoiContext):
    for check in _c.checks:
        try:
            if inspect.iscoroutinefunction(check):
                x = await check(ctx)
            else:
                x = check(ctx)
            if not x:
                return False
        except discord.DiscordException:
            return False
    else:
        return True


class Help(commands.Cog):
    def __init__(self, bot: aoi.AoiBot):
        self.bot = bot

    @property
    def description(self):
        return "Help module"

    @commands.command(brief="Lists Aoi's modules", aliases=["mdls"])
    async def modules(self, ctx: aoi.AoiContext):
        s = ""
        for grp_name, cogs in self.bot.cog_groups.items():
            if grp_name == "Hidden":
                continue
            s += f"\n**{grp_name}**\n"
            for cog in cogs:
                c = self.bot.get_cog(cog)
                if c.description:
                    s += f"◆ **{c.qualified_name}** - {c.description}\n"
        await ctx.embed(title="Modules", description=s.strip(),
                        footer=f"Do {ctx.clean_prefix}commands module_name to view commands in a module",
                        thumbnail=self.bot.user.avatar_url)

    @commands.command(brief="Lists commands within a module", name="commands",
                      aliases=["cmds"])
    async def cmds(self, ctx: aoi.AoiContext, module: str):
        cog: commands.Cog = self.bot.get_cog(self.bot.find_cog(module, check_description=True)[0])
        c: commands.Command
        await ctx.embed(
            title=f"Commands for {cog.qualified_name} module",
            description=cog.description + "\n\n" + "\n".join(
                [f"**{c.name}** - {c.brief}" for c in cog.get_commands() if await _can_run(c, ctx)]
            ),
            footer=f"Do {ctx.clean_prefix}help command_name for help on a command"
        )

    @commands.command(brief="Shows help for a command", aliases=["h"])
    async def help(self, ctx: aoi.AoiContext, command: str = None):
        if not command:
            return await ctx.embed(title="Aoi Help",
                                   fields=[("Module List", f"`{ctx.clean_prefix}modules` to view "
                                                           f"the list of Aoi's modules"),
                                           ("Module Commands", f"`{ctx.clean_prefix}commands module_name` "
                                                               f"to view commands in a module"),
                                           ("Permissions", f"`{ctx.clean_prefix}permguide` to view the "
                                                           f"permission guide"),
                                           ("Command Help", f"`{ctx.clean_prefix}help command_name` to "
                                                            f"view help for a command"),
                                           ("Other Guides", f"`{ctx.clean_prefix}cmds guides` to "
                                                            f"view other guides"),
                                           ("Support Server", f"Still need help? Join our [support "
                                                              f"server](https://discord.gg/pCgEj8t)")],
                                   not_inline=[0, 1, 2, 3, 4])
        cmd: commands.Command = self.bot.get_command(command.lower())
        if not cmd:
            return await ctx.send_error(f"Command `{command}` not found.")
        await ctx.embed(
            title=cmd.name,
            fields=[
                       ("Usage", f"`{cmd.name} {cmd.signature or ''}`"),
                       ("Description", cmd.brief),
                       ("Module", cmd.cog.qualified_name)
                   ] + (
                       [("Missing Permissions", "You are missing the permissions to run this command")]
                       if not await _can_run(cmd, ctx) else []
                   ) + (
                       [("Aliases", ", ".join([f"`{a}`" for a in cmd.aliases]))]
                       if cmd.aliases else []
                   ),
            footer="<> indicate required parameters, [] indicate optional parameters",
            not_inline=[0, 1, 2, 3]
        )


def setup(bot: aoi.AoiBot) -> None:
    bot.add_cog(Help(bot))
