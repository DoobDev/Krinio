import discord
import asyncio
from discord.ext import commands

from discord.ext.commands   import bot

token = input("Input your Discord Bot's token.\n")

client = commands.Bot(command_prefix = "!")

client.remove_command("help")

@client.event
async def on_ready():
    print('Among Us Bot is online!')
    await client.change_presence(status = discord.Status.online, activity=discord.Game('!help for commands'))

# Error handling.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Missing Requirement Error [DB10]", description="Pass in all required arguments.", colour=discord.Color.blue())

        await ctx.send(embed=embed)


    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Missing Permissions Error [DB11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.blue())

        await ctx.send(embed=embed)

# Ping command, gives latency of the bot to the user.
@client.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=":ping_pong:", colour=discord.Color.blue())

    embed.add_field(name="The latency for Among Us Bot is...", value=f"{round(client.latency * 1000)} ms")


    await ctx.send(embed=embed)

# Starts the game.
@client.command(aliases=['start'])
async def startgame(ctx):

    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"{ctx.author} is starting a lobby!", description="Click the checkmark to ready up!", colour=discord.Color.blue())

    await ctx.send('Game Starting! @everyone')
    message = await ctx.send(embed=embed)

    emojis = '✅'

    for emoji in emojis:
        await message.add_reaction(emoji)

@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    if user.bot:
        return

    if emoji == '✅':
        fixed_channel = client.get_channel(742888039872856067)
        await fixed_channel.send(f'{user.mention} is ready to play! [{reaction.count - 1}/10]')
    
@client.event
async def on_reaction_remove(reaction, user):
    emoji = reaction.emoji
    if user.bot:
        return

    if emoji == '✅':
        fixed_channel = client.get_channel(742888039872856067)
        await fixed_channel.send(f'{user.mention} is no longer ready to play! [{reaction.count - 1}/10]')
    
@client.command()
async def code(ctx):
    await ctx.channel.purge(limit=1)

    embed = discord.Embed(title='The Code for the game is:')

    embed.add_field(name='Code:', value=ctx.message.content.replace('!code ', ''))

    channel = client.get_channel(742889060179378217)
    await channel.purge(limit=1)
    await channel.send(embed=embed)

# Help command
@client.command(aliases=['commands'])
async def help(ctx):
    embed = discord.Embed(title='Among Us Bot Commands:', colour=discord.Color.blue())

    embed.add_field(name='Code', value='This command gives the members the code to the Among Us lobby, posted in #code.')
    embed.add_field(name='startgame', value='This command starts the game, and gives members the option to ready up!')
    embed.add_field(name='Ping', value='This shows the latency of the bot and the Discord Servers.')
    embed.add_field(name='cancelgame', value='Shows a message saying someone cancelled the lobby.')
    embed.add_field(name='FalseAlarm', value='You can blame someone for a false alarm.')

    await ctx.send(embed=embed)
    
@client.command(aliases=['cancel'])
async def cancelgame(ctx):
    embed = discord.Embed(title=f'{ctx.author} is cancelling the lobby', description='Go home.')

    await ctx.send(embed=embed)

@client.command()
async def falsealarm(ctx):
    embed = discord.Embed(title='False Alarm.', description=f'Blame {ctx.message.content.replace("!falsealarm ", "")}')

    channel = client.get_channel(742889060179378217)
    await channel.purge(limit=2)
    await channel.send(embed=embed)

    await ctx.send(embed=embed)

client.run(token)
