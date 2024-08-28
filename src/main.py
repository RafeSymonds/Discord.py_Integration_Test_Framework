import asyncio
import discord_interface


async def main():
    # Run bot - loops forever
    await discord_interface.client.start(discord_interface.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
