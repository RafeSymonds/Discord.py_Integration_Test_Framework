import sys
import os
import discord_interface

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import integration_test_framework.runner as runner

from discord.ext import commands

TEST_CHANNEL_ID = 1234567890
TEST_CHANNEL = discord_interface.client.get_channel(TEST_CHANNEL_ID)


async def test_most_recent_message(ctx: commands.Context):
    """TODO: Add docstring."""
    message = await ctx.send("!hello")
    await runner.process_bot_command(message)
    last_message = await discord_interface.get_last_message_for_channel(message.channel.id)
    assert last_message.content == f"Hello {discord_interface.client.user.mention}!"


async def test_most_recent_dm(ctx: commands.Context):
    """TODO: Add docstring."""
    await runner.process_bot_command()
