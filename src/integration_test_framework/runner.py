from typing import Callable
import discord
from discord.ext import commands
import pathlib
from inspect import getmembers, isfunction
from datetime import datetime, timedelta
import traceback


def display_time_delta(time: timedelta) -> str:
    milliseconds = time.microseconds // 1000
    seconds = time.seconds % 60
    minutes = time.seconds // 60

    formattedTime = ""

    if minutes > 1:
        formattedTime += f"{minutes} minutes "
    elif minutes == 1:
        formattedTime += f"{minutes} minute "
    formattedTime += f"{seconds}.{milliseconds} seconds"

    return formattedTime


class Integration_Test_Result:
    def __init__(
        self, test_name: str, passed: bool, error: str, total_time: timedelta
    ) -> None:
        self.test_name = test_name
        self.passed = passed
        self.error = error
        self.total_time = total_time

    def display_result(self) -> str:
        if self.passed:
            message = f"✅ {self.test_name} passed in {display_time_delta(self.total_time)}\n\n"
        else:
            message = f"❌ {self.test_name} failed in {display_time_delta(self.total_time)}\n{self.error}\n"

        return message


async def process_integration_test(
    test_name: str, test_function: Callable, ctx: commands.Context, test_num: int
) -> Integration_Test_Result:
    await ctx.send(f"```Test {test_num}: {test_name}```")

    start_time = datetime.now()

    try:
        await test_function()
    except Exception as e:
        total_time = datetime.now() - start_time

        return Integration_Test_Result(
            test_name,
            False,
            f"{e}, {type(e)}, {traceback.format_exc()}",
            total_time,
        )
    else:
        total_time = datetime.now() - start_time

        return Integration_Test_Result(test_name, True, "", total_time)


async def run_integration_tests(
    ctx: commands.Context,
    discord_user: discord.Member,
    integration_test_path: pathlib.Path,
    test_filter: str = "",
):
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

            test_result = await process_integration_test(
                function_name, function, ctx, test_num
            )

            test_results.append(test_results)

            test_num += 1

            if test_result.passed:
                tests_passed += 1

            await ctx.send(test_result.display_result())

    test_result_messages = [
        f"```Testing Results: {tests_passed}/{test_num} passed in {display_time_delta(datetime.now() - start_time)}\n"
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
