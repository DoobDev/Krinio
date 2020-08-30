import discord
from discord.ext import commands

codeid = input("Input your Discord Server's code channel id (again, same channel).\n")

class falsealarm(commands.Cog):
    def __init__(self, client):
        self.client = client
    # False Alarm command, puts a message in the code channel, and in the main chat that it was a false alarm.
    @commands.command()
    async def falsealarm(self, ctx):
        embed = discord.Embed(title='False Alarm.', description=f'Blame {ctx.message.content.replace("!falsealarm ", "")}')

        channel = client.get_channel(codeid) # Code channel.
        await channel.purge(limit=2)
        await channel.send(embed=embed)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(falsealarm(client))