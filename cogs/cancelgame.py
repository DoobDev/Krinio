import discord
from discord.ext import commands

class cancelgame(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Cancel game command, just cancels a lobby.
    @commands.command(aliases=['cancel'])
    async def cancelgame(self, ctx):
        embed = discord.Embed(title=f'{ctx.author} is cancelling the lobby', description='Go home.')

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(cancelgame(client))