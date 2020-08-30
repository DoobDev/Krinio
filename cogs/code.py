import discord
from discord.ext import commands

codeid = input("Input your Discord Server's code channel id.\n")

class code(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Code command, gives the code to code channel. Usage is !code {insert code here}
    @commands.command()
    async def code(self, ctx):
        await ctx.channel.purge(limit=1)

        embed = discord.Embed(title='The Code for the game is:')

        embed.add_field(name='Code:', value=f"||{ctx.message.content.replace('!code ', '')}||")

        channel = client.get_channel(codeid) # Code channel.
        await channel.purge(limit=1)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(code(client))