from asyncio import sleep
from glob import glob
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, Colour, Client, Intents
from discord.errors import Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context, when_mentioned_or, has_permissions
from discord.ext.commands import (
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
)
import os
from ..db import db  # pylint: disable=relative-beyond-top-level
from dotenv import load_dotenv

load_dotenv()

OWNER_IDS = [308000668181069824]
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        intents = discord.Intents.all()
        # Will need to go to discord.Intents.default if bot gets to 100+ servers.

        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            chunk_guilds_at_startup=True,
            intents=intents,
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[COGS] {cog} cog loaded!")

        print("Setup done!")

    def update_db(self):
        db.multiexec(
            "INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
            ((guild.id,) for guild in self.guilds),
        )
        db.commit()

    def run(self, version):
        self.VERSION = version

        print("Running setup!")
        self.setup()
        print("Authenticated...")
        print("Starting up")
        super().run(os.environ.get("TOKEN"), reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send(
                    "Please wait, Krinio hasn't fully started up yet", delete_after=10
                )

    async def on_connect(self):
        self.update_db()
        print("Krinio Connected")

    async def on_disconnect(self):
        print("Krinio Disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":

            raise err

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            await ctx.send(
                f"Something went wrong!\n\nError: {exc.original}", delete_after=10
            )

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Required arguments missing.", delete_after=10)

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f'That command is on a {str(exc.cooldown.type).split(".")[-1]} cooldown! Try again in {exc.retry_after:,.2f} seconds.',
                delete_after=exc.retry_after,
            )

        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send(
                    "Krinio doesn't have permissions to do that.", delete_after=10
                )

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            while not self.cogs_ready.all_ready():
                await sleep(1.0)

            db.multiexec(
                "INSERT OR IGNORE INTO users (UserID) VALUES (?)",
                (
                    (member.id,)
                    for guild in self.guilds
                    for member in guild.members
                    if not member.bot
                ),
            )
            print("Updated users table.")

            self.ready = True
            self.update_db

            print("Updated DB")
            print("Krinio Ready")

            meta = self.get_cog("Meta")
            await meta.set()

        else:
            print("Krinio Reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
