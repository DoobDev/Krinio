from discord import Embed, TextChannel

from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType, has_permissions, bot_has_permissions

from typing import Optional

from ..db import db # pylint: disable=relative-beyond-top-level

class Set(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="setlogchannel", aliases=["slc", "logchannel", "setlog", "setlogs"], brief="Set the server's log channel.")
	@has_permissions(manage_guild=True)
	async def set_log_channel(self, ctx, *, channel: Optional[TextChannel]):
		"""Sets the logging channel for the server.\n`Manage Server` permission required."""
		current_channel = db.records("SELECT LogChannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
		prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

		if channel == None:
			await ctx.send(f"The current setting for the Log Channel is currently: <#{current_channel[0][0]}>\nTo change it, type `{prefix[0][0]}setlogchannel #<log channel>`")

		else:
			db.execute("UPDATE guilds SET LogChannel = ? WHERE GuildID = ?", str(channel.id), ctx.guild.id)
			db.commit()
			await ctx.send(f"Log channel set to <#{channel.id}>")

	@command(name="setcodechannel", aliases=["scc", "codechannel", "setcode"], brief="Set the server's code channel.")
	@has_permissions(manage_guild=True)
	async def set_code_channel(self, ctx, *, channel: Optional[TextChannel]):
		"""Sets the code for the server.\n`Manage Server` permission required."""
		current_channel = db.records("SELECT CodeChannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
		prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

		if channel == None:
			await ctx.send(f"The current setting for the Code Channel is currently: <#{current_channel[0][0]}>\nTo change it, type `{prefix[0][0]}setcodechannel #<log channel>`")

		else:
			db.execute("UPDATE guilds SET CodeChannel = ? WHERE GuildID = ?", str(channel.id), ctx.guild.id)
			db.commit()
			await ctx.send(f"Code channel set to <#{channel.id}>")

	@command(name="setreadyupchannel", aliases=["sruc", "readyupchannel", "setreadyup", "src", "setreadychannel", "readychannel", "setready"], brief="Set the server's code channel.")
	@has_permissions(manage_guild=True)
	async def set_ready_channel(self, ctx, *, channel: Optional[TextChannel]):
		"""Sets the ready up channel for the server.\n`Manage Server` permission required."""
		current_channel = db.records("SELECT ReadyUpChannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
		prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

		if channel == None:
			await ctx.send(f"The current setting for the Ready Up Channel is currently: <#{current_channel[0][0]}>\nTo change it, type `{prefix[0][0]}setreadyupchannel #<log channel>`")

		else:
			db.execute("UPDATE guilds SET ReadyUpChannel = ? WHERE GuildID = ?", str(channel.id), ctx.guild.id)
			db.commit()
			await ctx.send(f"Code channel set to <#{channel.id}>")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("set")

def setup(bot):
	bot.add_cog(Set(bot))