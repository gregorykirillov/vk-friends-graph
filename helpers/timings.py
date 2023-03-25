from datetime import datetime
import asyncio

from config import TIME_TO_SLEEP


class Timings():
    def __init__(self):
        self.last_time = datetime.now()

    def set_new_last_time(self):
        self.last_time = datetime.now()

    def get_last_time(self):
        return self.last_time

    async def sleep(self):
        taken_time = (datetime.now() - self.get_last_time()).total_seconds()

        if taken_time < TIME_TO_SLEEP:
            print(f'Taked {taken_time} sec')
            print(f'Sleeping {TIME_TO_SLEEP - taken_time}')
            await asyncio.sleep(TIME_TO_SLEEP - taken_time)

        self.set_new_last_time()
