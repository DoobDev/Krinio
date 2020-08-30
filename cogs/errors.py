import discord
from discord.ext import commands

class errors(commands.Cog):
    def __init__(self, client):
        self.client = client    
    
    # Error handling.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Missing Requirement Error [DB10]", description="Pass in all required arguments.", colour=discord.Color.blue())

            embed.add_field(name="Docs", value="Check out the Docs for more info. - http://docs.doobbot.com/")

            await ctx.send(embed=embed)

        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions Error [DB11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.blue())

            embed.add_field(name="Docs", value="Check out the Docs for more info. - http://docs.doobbot.com/")

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(errors(client))