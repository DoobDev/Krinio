from discord import Embed

from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType

from ..db import db # pylint: disable=relative-beyond-top-level

class Game(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="code", aliases=["entercode", "gamecode"], brief="Gives out the game's code")
    @cooldown(1, 10, BucketType.user)
    async def code_command(self, ctx, *, code: str):
        """Gives the game's code to the code channel"""

        await ctx.channel.purge(limit=1)
        
        embed = Embed(title="The code for the game is:", description=code, colour=ctx.author.colour)
        embed.set_footer(text=f"Authored by: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        code_channel = await self.bot.fetch_channel(db.field("SELECT CodeChannel FROM guilds WHERE GuildID = ?", ctx.guild.id))
        await code_channel.send(embed=embed)
        await ctx.send(f"Code sent {ctx.author.mention}", delete_after=10)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("game")

def setup(bot):
    bot.add_cog(Game(bot))