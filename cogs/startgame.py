import discord
from discord.ext import commands

generalid = input("Input your Discord Server's main/general channel id.\n")

class startgame(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Starts the game.
    @commands.command(aliases=['start'])
    async def startgame(self, ctx):

        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title=f"{ctx.author} is starting a lobby!", description="Click the checkmark to ready up!", colour=discord.Color.blue())

        await ctx.send('Game Starting! @everyone')
        message = await ctx.send(embed=embed)

        emojis = '✅'

        for emoji in emojis:
            await message.add_reaction(emoji)


    # Reaction events.
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        if user.bot:
            return

        if emoji == '✅':
            fixed_channel = client.get_channel(generalid) # General / main chat channel ID
            await fixed_channel.send(f'{user.mention} is ready to play! [{reaction.count - 1}/10]')

def setup(client):
    client.add_cog(startgame(client))