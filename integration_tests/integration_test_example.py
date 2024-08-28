import discord_interface as di
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import integration_test_framework.runner as runner

TEST_CHANNEL_ID = 1234567890
TEST_CHANNEL = di.client.get_channel(TEST_CHANNEL_ID)


async def test_most_recent_message(ctx):
    message = await ctx.send("!hello")
    await runner.process_bot_command(message)
    last_message = await di.get_last_message_for_channel(message.channel.id)
    assert last_message.content == "Hello <@1278404785464283290>!"
