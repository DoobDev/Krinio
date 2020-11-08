from discord import Embed

from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType, has_permissions

from discord.ext import menus

from discord.utils import get

from ..db import db # pylint: disable=relative-beyond-top-level

class GameMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        embed = Embed(title="Game Starting", colour=ctx.author.colour)
        embed.set_footer(text=f"Started By: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.set_author(name="✅ - Ready Up | ⏹ - Clear Reactions")
        return await channel.send(embed=embed)

    @menus.button('✅')
    async def on_checkmark(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        await self.message.edit(content=f"{reaction.count - 1}/10 ready.")
        if reaction and reaction.count >= 10:
            await message.clear_reactions()

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()

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

    @command(name="startgame", aliases=["start"], brief="Lets the user start a game.")
    @cooldown(1, 4, BucketType.user)
    async def start_game(self, ctx):
        """Starts a game that lets people ready up!"""
        ping = db.record("SELECT Ping from guilds WHERE GuildID = ?", ctx.guild.id)

        m = GameMenu(clear_reactions_after=True)
        await m.start(ctx)

        await ctx.send(f"{ping[0]} Game is starting!~")

    @command(name="startgamenoping", aliases=["noping", "startnoping"], brief="Lets the user start a game without a ping.")
    @cooldown(1, 4, BucketType.user)
    @has_permissions(mention_everyone = True)
    async def start_game_no_pint(self, ctx):
        """Starts a game that lets people ready up without a ping!"""

        m = GameMenu(clear_reactions_after=True)
        await m.start(ctx)

        await ctx.send(f"Game is starting!~")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("game")

def setup(bot):
    bot.add_cog(Game(bot))