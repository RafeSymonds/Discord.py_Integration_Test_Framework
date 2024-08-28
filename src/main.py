import asyncio
import discord_interface


async def main():
    # Run bot - loops forever
    if globals()["RELEASE_VERSION"]:  # Run official bot
        await discord_interface.client.start(discord_interface.BOT_COMAMND_PREFIX)
    else:  # Run test bot
        await discord_interface.client.start(discord_interface.BOT_COMAMND_PREFIX)


if __name__ == "__main__":
    asyncio.run(main())
