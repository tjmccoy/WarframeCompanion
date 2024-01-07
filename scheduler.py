import datetime
import asyncio

def scheduled(on_hour: str | int = "any", on_minute: str | int = "any", on_second: str | int = "any"):
    def schedule(func):
        async def inner():
            await func()
            await asyncio.sleep(1)
            now = datetime.datetime.utcnow()
            hours_until = 0 if on_hour == "any" else (on_hour - now.hour) % 24
            minutes_until = 0 if on_minute == "any" else (on_minute - now.minute) % 60
            seconds_until = 0 if on_second == "any" else (on_second - now.second) % 60
            delay = datetime.timedelta(hours = hours_until, minutes = minutes_until, seconds = seconds_until).total_seconds()
            await asyncio.sleep(delay)
            asyncio.create_task(inner())
        return inner
    return schedule
