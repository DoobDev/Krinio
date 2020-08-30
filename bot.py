# Doob Dev 2020
import discord
import asyncio
import os
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


@client.command()
async def load(ctx, extension):
    print(f'Loaded {extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Loaded {extension}')

@client.command()
async def unload(ctx, extension):
    print(f'Unloaded {extension}')
    client.unload_extension(f'cogs.{extension}')
    print(f'Unloaded {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

client.run(token)
