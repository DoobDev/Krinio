# Doob Dev 2020 - Privated Bot
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands   import bot

token = input("Input your Discord Bot's token.\n")

client = commands.Bot(command_prefix = "!")

client.remove_command("help")

# Starts the bot, with a status.
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
    embed = discord.Embed(title=f"{ctx.author.name} is starting a lobby!", description="Click the checkmark to ready up!", colour=discord.Color.blue())
    embed.set_footer(text=f"Started By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send('Game Starting! @everyone')
    message = await ctx.send(embed=embed)
    emojis = '✅'
    for emoji in emojis:
        await message.add_reaction(emoji)

# Reaction events
@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == "Among Us Bot#3079":
        emoji = reaction.emoji
        if user.bot:
            return
        if emoji == '✅':
            fixed_channel = client.get_channel(742888039872856067) # General / main chat channel ID
            await fixed_channel.send(f'{user.mention} is ready to play! [{reaction.count - 1}/10]')
    else:
        print("BRUH")


@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.author == "Among Us Bot#3079":
        emoji = reaction.emoji
        if user.bot:
            return
        if emoji == '✅':
            fixed_channel = client.get_channel(742888039872856067) # General / main chat channel ID
            await fixed_channel.send(f'{user.mention} is no longer ready to play! [{reaction.count - 1}/10]')
    else:
        print("BRUH x2")


# Code command, gives the code to code channel. Usage is !code {insert code here}
@client.command()
async def code(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='The Code for the game is:')
    embed.add_field(name='Code:', value=f"{ctx.message.content.replace('!code ', '')}")
    channel = client.get_channel(742889060179378217) # Code channel.
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
    embed.add_field(name='StartGameNoPing', value='Starts the game, with no ping.')
    embed.add_field(name='ImposterWon', value='!imposterwon {imposters}. Shows who the imposters were, and when they won!')
    embed.add_field(name='CrewWon', value='!crewwon {imposters}. Shows that the crew won and who the imposters were.')
    await ctx.send(embed=embed)


# Cancel game command, just cancels a lobby.
@client.command(aliases=['cancel'])
async def cancelgame(ctx):
    embed = discord.Embed(title=f'{ctx.author} is cancelling the lobby', description='Go home.')
    await ctx.send(embed=embed)


# False Alarm command, puts a message in the code channel, and in the main chat that it was a false alarm.
@client.command()
async def falsealarm(ctx):
    embed = discord.Embed(title='False Alarm.', description=f'Blame {ctx.message.content.replace("!falsealarm ", "")}')
    channel = client.get_channel(742889060179378217) # Code channel.
    await channel.purge(limit=2)
    await channel.send(embed=embed)
    await ctx.send(embed=embed)


# This is a copy paste of the start game, except without the @everyone ping.
@client.command(aliases=['noping', 'startnoping'])
async def startgamenoping(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"{ctx.author.name} is starting a lobby!", description="Click the checkmark to ready up!", colour=discord.Color.blue())
    embed.set_footer(text=f"Started By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send('Game Starting!')
    message = await ctx.send(embed=embed)
    emojis = '✅'
    for emoji in emojis:
        await message.add_reaction(emoji)

@client.command()
async def crewwon(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Imposters Lost!', colour=discord.Color.red())
    embed.add_field(name="Imposters:", value=ctx.message.content.replace("!crewwon ", ""))
    embed.add_field(name="Timestamp:", value=ctx.message.created_at, inline=True)
    embed.set_thumbnail(url = "https://static.thenounproject.com/png/158126-200.png")
    embed.set_footer(text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def imposterwon(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Congragulations Imposters!!', colour=discord.Color.gold())
    embed.add_field(name="Imposters:", value=ctx.message.content.replace("!imposterwon ", ""))
    embed.add_field(name="Timestamp:", value=ctx.message.created_at, inline=True)
    embed.set_thumbnail(url = "https://image.flaticon.com/icons/png/512/419/419952.png")
    embed.set_footer(text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

client.run(token)