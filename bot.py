# Doob Dev 2020 - Privated Bot
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands   import bot
from datetime import datetime

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
        await ctx.send(embed=embed, delete_after = 15)

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Missing Permissions Error [DB11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.blue())
        await ctx.send(embed=embed, delete_after = 15)

    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown", description="You are on cooldown! Please try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed, delete_after = error.retry_after)

    if isinstance(error, commands.ArgumentParsingError):
        embed = discord.Embed(title="Argument Parsing Error [DB12]", description="An exception raised when the parser fails to parse a user’s input.", colour=discord.Color.red())
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
        await ctx.send(embed=embed, delete_after= 15)

    if isinstance(error, commands.PrivateMessageOnly):
        embed = discord.Embed(title="Private Message Only [DB13]", description="This command does not work in a server, only in PMs")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
        await ctx.send(embed=embed, delete_after= 15)

    if isinstance(error, commands.NoPrivateMessage):
        embed=discord.Embed(title="No Private Message [DB14]", description="This command doesn't work in PMs")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
        await ctx.send(embed=embed, delete_after= 15)

    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(title="Command Disabled [DB15]", description="This command has been disabled.")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
        await ctx.send(embed=embed, delete_after= 15)

    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(title="Not Owner [DB16]", description="This is a owner only command.")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
        await ctx.send(embed=embed, delete_after= 15)

    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title="Bot Missing Permissions [DB17]", description="Doob is missing permissions, that are needed to execute this command.")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
        await ctx.send(embed=embed, delete_after= 15)
    else:
        raise error

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
@commands.cooldown(1, 10, commands.BucketType.user)
async def on_reaction_add(reaction, user):
    if reaction.message.author.id == client.user.id:
        emoji = reaction.emoji
        if user.bot:
            return
        if emoji == '✅':
            fixed_channel = client.get_channel(742888039872856067) # General / main chat channel ID
            await fixed_channel.send(f'{user.mention} is ready to play! [{reaction.count - 1}/10]')
    else:
        print("BRUH")


@client.event
@commands.cooldown(1, 10, commands.BucketType.user)
async def on_reaction_remove(reaction, user):
    if reaction.message.author.id == client.user.id:
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
@commands.cooldown(1, 10, commands.BucketType.user)
async def code(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='The Code for the game is:')
    embed.add_field(name='Code:', value=f"{ctx.message.content.replace('!code ', '')}")
    embed.set_footer(text=f"Code By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    channel = client.get_channel(742889060179378217) # Code channel.
    await channel.purge(limit=1)
    await channel.send(embed=embed)


# Help command
@client.command(aliases=['commands'])
@commands.cooldown(1, 10, commands.BucketType.user)
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
    embed.add_field(name="Patreon", value="Support the developer of the Among Us Bot on Patreon! https://patreon.com/doobdev")
    embed.set_footer(text="This bot was made by: mmatt#0001", icon_url="https://cdn.discordapp.com/avatars/308000668181069824/90f0120c5408f595953e035df9b453a4.webp?size=1024")
    await ctx.send(embed=embed)

# Patreon Command
@client.command(aliases=['donate'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def patreon(ctx):
    embed = discord.Embed(title="The developer's Patreon is avaliable at:", description="https://patreon.com/doobdev")
    embed.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/a3z1idZDuso6ksgW6pDOZwCRJDw=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/9833961/patreon.jpg")
    embed.set_footer(text="mmatt thanks you! (doob luvs yuh)", icon_url="https://cdn.discordapp.com/avatars/308000668181069824/90f0120c5408f595953e035df9b453a4.webp?size=1024")
    await ctx.send(embed=embed)

# Cancel game command, just cancels a lobby.
@client.command(aliases=['cancel'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def cancelgame(ctx):
    embed = discord.Embed(title=f'{ctx.author} is cancelling the lobby', description='Go home.')
    await ctx.send(embed=embed)


# False Alarm command, puts a message in the code channel, and in the main chat that it was a false alarm.
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def falsealarm(ctx):
    embed = discord.Embed(title='False Alarm.', description=f'Blame {ctx.message.content.replace("!falsealarm ", "")}')
    channel = client.get_channel(742889060179378217) # Code channel.
    await channel.purge(limit=2)
    await channel.send(embed=embed)
    await ctx.send(embed=embed)


# This is a copy paste of the start game, except without the @everyone ping.
@client.command(aliases=['noping', 'startnoping'])
@commands.cooldown(1, 10, commands.BucketType.user)
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
@commands.cooldown(1, 10, commands.BucketType.user)
async def crewwon(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Imposters Lost!', colour=discord.Color.red(), timestamp=datetime.utcnow())
    embed.add_field(name="Imposters:", value=ctx.message.content.replace("!crewwon ", ""))
    embed.set_thumbnail(url = "https://static.thenounproject.com/png/158126-200.png")
    embed.set_footer(text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def imposterwon(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Congragulations Imposters!!', colour=discord.Color.gold(), timestamp=datetime.utcnow())
    embed.add_field(name="Imposters:", value=ctx.message.content.replace("!imposterwon ", ""))
    embed.set_thumbnail(url = "https://image.flaticon.com/icons/png/512/419/419952.png")
    embed.set_footer(text=f"Reported By: {ctx.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def credits(ctx):
    embed=discord.Embed(title='This bot was created by:', colour=discord.Color.blue())
    embed.add_field(name="mmatt#0001", value="", inline=True)
    embed.set_thumbnail(url = "https://cdn.discordapp.com/avatars/308000668181069824/90f0120c5408f595953e035df9b453a4.webp?size=1024")
    embed.set_footer(text='github.com/mmattbtw')
    await ctx.send(embed=embed)

client.run(token)
