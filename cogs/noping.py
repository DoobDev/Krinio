import discord
from discord.ext import commands

class noping(commands.Cog):
    def __init__(self, client):
        self.client = client
    # This is a copy paste of the start game, except without the @everyone ping.
    @commands.command(aliases=['noping', 'startnoping'])
    async def startgamenoping(self, ctx):

        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title=f"{ctx.author} is starting a lobby!", description="Click the checkmark to ready up!", colour=discord.Color.blue())

        await ctx.send('Game Starting!')
        message = await ctx.send(embed=embed)

        emojis = '✅'

        for emoji in emojis:
            await message.add_reaction(emoji)

def setup(client):
    client.add_cog(noping(client))