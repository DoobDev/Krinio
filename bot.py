import discord
from discord.ext import commands

token = input("Input your Discord Bot's token.")

client = commands.Bot(command_prefix = "!")

client.remove_command("help")

@client.event
async def on_ready():
    print('Among Us Bot is online!')
    await client.change_presence(status = discord.Status.online, activity=discord.Game('!help for commands'))


# Error handling.
@commands.Cog.listener()
async def on_command_error(self, ctx, error):
if isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(title="Missing Requirement Error [DB10]", description="Pass in all required arguments.", colour=discord.Color.blue())

    embed.add_field(name="Docs", value="Check out the Docs for more info. - http://docs.doobbot.com/")

    embed.set_thumbnail(url=doob_logo)
    await ctx.send(embed=embed)


if isinstance(error, commands.MissingPermissions):
    embed = discord.Embed(title="Missing Permissions Error [DB11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.blue())

    embed.add_field(name="Docs", value="Check out the Docs for more info. - http://docs.doobbot.com/")

    embed.set_thumbnail(url=doob_logo)
    await ctx.send(embed=embed)


@client.command

client.run(token)