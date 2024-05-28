"""Logger for all sended messages."""
from Bots.BotBase import BotBase
from _i18n import _
import asyncio
import aiofiles as aiof


class Logger(BotBase):
    """Logger for all sended messages."""

    def __init__(self, parameters):
        """Set up log file path from parameters."""
        self.path = parameters["logPath"]
        print(_("Created Logger"))

    async def start(self):
        """Do nothing."""
        while True:
            await asyncio.sleep(0)

    def base_message_handler(self, msg):
        """Do nothing."""
        pass

    async def send(self, message):
        """
        Write message to log file.

        :param message: message to write
        """
        async with aiof.open(self.path, "a") as log_file:
            log = ' '.join([message.date.strftime('%d-%m-%Y %H:%M:%S'),
                            message.source,
                            message.author,
                            message.text, '\n'])
            await log_file.write(log)
