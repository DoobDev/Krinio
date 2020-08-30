import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Help command.
    @commands.command(aliases=['commands'])
    async def help(self, ctx):
        embed = discord.Embed(title='Among Us Bot Commands:', colour=discord.Color.blue())

        embed.add_field(name='Code', value='This command gives the members the code to the Among Us lobby, posted in #code.')
        embed.add_field(name='startgame', value='This command starts the game, and gives members the option to ready up!')
        embed.add_field(name='Ping', value='This shows the latency of the bot and the Discord Servers.')
        embed.add_field(name='cancelgame', value='Shows a message saying someone cancelled the lobby.')
        embed.add_field(name='FalseAlarm', value='You can blame someone for a false alarm.')
        embed.add_field(name='StartGameNoPing', value='Starts the game, with no ping.')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))