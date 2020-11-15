from discord import Embed

from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType, has_permissions

from ..db import db # pylint: disable=relative-beyond-top-level

class Overlay(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="overlay", brief="Gives Discord Streamkit Overlay.")
    @cooldown(1, 5, BucketType.user)
    async def streamkit_overlay_command(self, ctx):
        """Gives a Discord Streamkit Overlay link for your Livestreams"""
        
        # super long URL so im just making it into a variable 
        streamkit_url = f"https://streamkit.discord.com/overlay/voice/{ctx.guild.id}/{ctx.author.voice.channel.id}?icon=true&online=true&logo=white&text_color=%23ffffff&text_size=14&text_outline_color=%23000000&text_outline_size=0&text_shadow_color=%23000000&text_shadow_size=0&bg_color=%231e2124&bg_opacity=0.95&bg_shadow_color=%23000000&bg_shadow_size=0&invite_code=&limit_speaking=false&small_avatars=false&hide_names=false&fade_chat=0"

        embed = Embed(title="Straemkit Overlay:", description=streamkit_url, colour=ctx.author.colour, timestamp=datetime.utcnow())
        embed.set_footer(text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/OBS.svg/1024px-OBS.svg.png")
        await ctx.send(embed=embed)

    @streamkit_overlay_command.error
    async def streamkit_overlay_command_error(self, ctx, exc):
        if hasattr(exc, "original"):
            if isinstance(exc.original, AttributeError):
                await ctx.message.delete()
                await ctx.send("Please join a voice channel before running the `overlay` command.", delete_after=15)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("overlay")

def setup(bot):
    bot.add_cog(Overlay(bot))