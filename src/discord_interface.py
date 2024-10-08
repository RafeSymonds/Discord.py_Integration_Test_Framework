import discord
from discord.ext import commands
import asyncio
import pathlib

from discord.webhook import async_
import integration_test_framework.runner as runner

BOT_COMAMND_PREFIX = "!"
RETRY_LIMIT_AMOUNT = 10
BOT_TOKEN = "MTI3ODQwNDc4NTQ2NDI4MzI5MA.GABipK.YjCrmLP49pIloEVTyg2QyrYqR9eHOeoJfOgImI"

# Set up client and intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(intents=intents, command_prefix=BOT_COMAMND_PREFIX)

# Having this enabled caused problems
"""
@client.event
async def on_message(message: discord.Message):
    await runner.process_bot_command(message)
    await client.process_commands(message)
"""


@commands.command()
async def hello(ctx: commands.Context):
    """TODO: Add docstring."""
    await ctx.message.channel.send(f"Hello {ctx.message.author.mention}!")


@commands.command()
async def run_tests(ctx: commands.Context):
    """TODO: Add docstring."""
    await runner.run_integration_tests(ctx, ctx.message.author, pathlib.Path("integration_tests"))


@commands.command()
async def dm_hello(ctx: commands.Context):
    """TODO: Add docstring."""
    user = ctx.message.author
    channel = await user.create_dm()
    await channel.send(f"Hello in DM {user.mention}!")


client.add_command(hello)
client.add_command(run_tests)
client.add_command(dm_hello)


async def send_message(msg: str, channel: discord.channel.TextChannel | discord.channel.DMChannel) -> None:
    await channel.send(msg)


async def wait_for_new_message_in_same_channel(sent_message):
    retry_limit = RETRY_LIMIT_AMOUNT
    while retry_limit > 0:
        async for message in sent_message.channel.history(limit=1):
            if message.id != sent_message.id:
                return message
            break
        if retry_limit > 0:
            retry_limit -= 1
            await asyncio.sleep(0.5)
    raise Exception("Expected message was never sent")


async def wait_for_new_message_in_DM(last_message_id: int, discord_id: int, reaction_count: int = 0):
    retry_limit = RETRY_LIMIT_AMOUNT
    while retry_limit > 0:
        discord_user = await client.fetch_user(discord_id)
        channel = await discord_user.create_dm()
        async for message in channel.history(limit=1):
            if message.id != last_message_id and len(message.reactions) >= reaction_count:
                return message
            break
        if retry_limit > 0:
            retry_limit -= 1
            await asyncio.sleep(0.5)
    raise Exception("Expected message in DM was never sent")


async def get_last_message_for_channel(channel_id) -> discord.Message | None:
    channel = client.get_channel(channel_id)
    if channel is None:
        channel = await client.fetch_channel(channel_id)

    async for message in channel.history(limit=1):
        return message

    return None


async def get_last_message_for_user(discord_id: int) -> discord.Message | None:
    discord_user = await client.fetch_user(discord_id)
    channel = await discord_user.create_dm()

    async for message in channel.history(limit=1):
        return message
