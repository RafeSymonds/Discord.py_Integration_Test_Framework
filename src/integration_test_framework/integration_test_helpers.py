from datetime import timedelta
import discord


def __display_time_delta(time: timedelta) -> str:
    milliseconds = time.microseconds // 1000
    seconds = time.seconds % 60
    minutes = time.seconds // 60

    formatted_time = ""

    if minutes > 1:
        formatted_time += f"{minutes} minutes "
    elif minutes == 1:
        formatted_time += f"{minutes} minute "
    formatted_time += f"{seconds}.{milliseconds} seconds"

    return formatted_time


class IntegrationTestResult:
    def __init__(
        self,
        test_name: str,
        passed: bool,
        error: str,
        total_time: timedelta,
    ) -> None:
        self.test_name = test_name
        self.passed = passed
        self.error = error
        self.total_time = total_time

    def display_result(self) -> str:
        if self.passed:
            message = f"✅ {self.test_name} passed in {__display_time_delta(self.total_time)}\n\n"
        else:
            message = f"❌ {self.test_name} failed in {__display_time_delta(self.total_time)}\n{self.error}\n"

        return message


class IntegrationTestInfo:
    def __init__(self, discord_user_overwrite: discord.Member | None) -> None:
        self.discord_user_overwrite = discord_user_overwrite
