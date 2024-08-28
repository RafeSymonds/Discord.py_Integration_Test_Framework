import discord
from discord.ext import commands

BOT_COMAMND_PREFIX = "!"


# Set up client and intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(intents=intents, command_prefix=BOT_COMAMND_PREFIX)


async def send_message(msg: str, channel: discord.channel.TextChannel | discord.channel.DMChannel) -> None:
    await channel.send(msg)
