import discord_interface as di

TEST_CHANNEL_ID = 1234567890
TEST_CHANNEL = di.client.get_channel(TEST_CHANNEL_ID)


async def test_most_recent_message():
    message = await TEST_CHANNEL.send("! Hello World!")

    assert di.get_last_message_for_channel(message) == "Hello World Again!"
