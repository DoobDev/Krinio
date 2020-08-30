import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Gives ping to the user.
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=":ping_pong:", colour=discord.Color.blue())

        embed.add_field(name="The latency for Among Us Bot is...", value=f"{round(client.latency * 1000)} ms")


        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(ping(client))