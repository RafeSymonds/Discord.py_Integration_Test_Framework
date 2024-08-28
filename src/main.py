import asyncio
import discord_interface
import integration_test_framework.runner as runner
import discord


async def main():
    # Run bot - loops forever
    await discord_interface.client.start(discord_interface.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
