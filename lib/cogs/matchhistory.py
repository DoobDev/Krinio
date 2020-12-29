from discord import Embed, Color

from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType, has_permissions

from ..db import db  # pylint: disable=relative-beyond-top-level


class MatchHistory(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="crewwon", brief="Shows who the imposters were when crew won!")
    @cooldown(1, 5, BucketType.user)
    async def crew_won(self, ctx):
        feed = await self.bot.fetch_channel(
            db.field("SELECT MatchHistory from guilds WHERE GuildID = ?", ctx.guild.id)
        )

        await ctx.channel.purge(limit=1)

        embed = Embed(
            title="Imposters Lost!", colour=Color.red(), timestamp=datetime.utcnow()
        )
        embed.set_footer(
            text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url
        )

        await feed.send(embed=embed)

    @command(name="imposterwon", brief="Shows who the imposters were when they won!")
    @cooldown(1, 5, BucketType.user)
    async def imposter_won(self, ctx):
        feed = await self.bot.fetch_channel(
            db.field("SELECT MatchHistory from guilds WHERE GuildID = ?", ctx.guild.id)
        )

        await ctx.channel.purge(limit=1)

        embed = Embed(
            title="Imposters Won!", colour=Color.gold(), timestamp=datetime.utcnow()
        )
        embed.set_footer(
            text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url
        )

        await feed.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("matchhistory")


def setup(bot):
    bot.add_cog(MatchHistory(bot))
