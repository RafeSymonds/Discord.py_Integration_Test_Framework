# TODO: update doc string
"""Frame work."""

import pathlib
import traceback
from collections.abc import Callable
from datetime import datetime
from inspect import getmembers, isfunction

import discord
import discord_interface
import integration_test_helpers
from discord.ext import commands

__test_info: integration_test_helpers.IntegrationTestInfo = (
    integration_test_helpers.IntegrationTestInfo(None)
)


async def __process_integration_test(
    test_name: str,
    test_function: Callable,
    ctx: commands.Context,
    test_num: int,
) -> integration_test_helpers.IntegrationTestResult:
    await ctx.send(f"```Test {test_num}: {test_name}```")

    start_time = datetime.now()

    try:
        await test_function()
    except Exception as e:
        total_time = datetime.now() - start_time

        return integration_test_helpers.IntegrationTestResult(
            test_name,
            False,
            f"{e}, {type(e)}, {traceback.format_exc()}",
            total_time,
        )
    else:
        total_time = datetime.now() - start_time

        return integration_test_helpers.IntegrationTestResult(
            test_name, True, "", total_time
        )


def test_setup(discord_user: discord.Member) -> None:
    """Run before every test."""
    __test_info = integration_test_helpers.IntegrationTestInfo(
        discord_user
    )


async def run_integration_tests(
    ctx: commands.Context,
    discord_user: discord.Member,
    integration_test_path: pathlib.Path,
    test_filter: str = "",
) -> None:
    # TODO: update doc string
    """Run all integration tests that contain test_filter."""
    test_setup(discord_user)

    integration_test_files = [
        item for item in integration_test_path.iterdir() if item.is_file()
    ]

    test_num = 1
    tests_passed = 0

    start_time = datetime.now()

    test_results = []

    for file_path in integration_test_files:
        tests = getmembers(file_path, isfunction)

        for function_name, function in tests:
            if not function_name.startswith("test"):
                continue
            if function_name.lower().find(test_filter) == -1:
                continue

            test_result = await __process_integration_test(
                function_name,
                function,
                ctx,
                test_num,
            )

            test_results.append(test_results)

            test_num += 1

            if test_result.passed:
                tests_passed += 1

            await ctx.send(test_result.display_result())

    test_result_messages = [
        f"```Testing Results: {tests_passed}/{test_num} passed in {integration_test_helpers.__display_time_delta(datetime.now() - start_time)}\n",
    ]

    for test_result in test_results:
        message = test_result.display_result()
        if len(test_result_messages[-1]) + len(message) > 1950:
            test_result_messages[-1] += "```"
            test_result_messages.append("```")

        test_result_messages.append(f"\t{message}")

        if test_result_messages[-1][-1] != "`":
            test_result_messages[-1] += "```"

    for message in test_result_messages:
        await ctx.send(message)


async def should_overwrite_bot(status: bool):
    __test_info.overwrite_user(status)


async def process_bot_command(message: discord.Message) -> None:
    # TODO: upadate doc string
    """Process bot commands from on_message client event."""
    if message.author != discord_interface.client.user:
        return

    if message.content.startswith(
        f"{discord_interface.BOT_COMAMND_PREFIX}"
    ):
        return

    if __test_info.discord_user_overwrite is None:
        return

    ctx = await discord_interface.client.get_context(message)
    ctx.prefix = discord_interface.BOT_COMAMND_PREFIX
    command_name = message.content[3:]
    ctx.command = discord_interface.client.get_command(command_name)

    ctx.message.author = __test_info.discord_user_overwrite
    ctx.author = __test_info.discord_user_overwrite

    await discord_interface.client.invoke(ctx)
