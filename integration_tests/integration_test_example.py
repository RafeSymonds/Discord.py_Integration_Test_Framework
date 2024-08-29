import sys
import os
import discord_interface

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import integration_test_framework.runner as runner

from discord.ext import commands


async def test_most_recent_message(ctx: commands.Context):
    """TODO: Add docstring."""
    message = await ctx.send("!hello")
    await runner.process_bot_command(message)
    last_message = await discord_interface.get_last_message_for_channel(message.channel.id)
    assert last_message.content == f"Hello {discord_interface.client.user.mention}!"


async def test_most_recent_dm(ctx: commands.Context):
    """TODO: Add docstring."""
    message = await ctx.send("!dm_hello")
    await runner.process_bot_command(message)
    discord_id = ctx.message.author.id
    last_dm = await discord_interface.get_last_message_for_user(discord_id)
    last_message = await discord_interface.wait_for_new_message_in_DM(last_dm, discord_id)
    assert last_message.content == f"Hello in DM {ctx.message.author.mention}!"
