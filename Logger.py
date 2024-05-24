from BotBase import BotBase
import asyncio
import aiofiles as aiof

class Logger(BotBase):
    def __init__(self, parameters):
        self.path = parameters["logPath"]
        print("Created Logger")
    
    async def start(self):
        while True:
            await asyncio.sleep(0)
    
    def base_message_handler(self, msg):
        pass

    async def send(self, msg):
        async with aiof.open(self.path, "a") as log_file:
            await log_file.write(msg + "\n")
    