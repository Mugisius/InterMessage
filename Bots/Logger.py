from Bots.BotBase import BotBase
import asyncio
import aiofiles as aiof

class Logger(BotBase):
    def __init__(self, parameters):
        self.path = parameters["logPath"]
        print("Created Logger")
    
    async def start(self):
        while True:
            await asyncio.sleep(0)

    def get_attachments(self):
        pass
    
    def base_message_handler(self, message):
        pass

    async def send(self, msg):
        async with aiof.open(self.path, "a") as log_file:
            if msg.text == None:
                text = "Has no text"
            else:
                text = msg.text

            log = ' '.join([ msg.date.strftime('%d-%m-%Y %H:%M:%S'),
                             msg.source,
                             msg.author,
                             text, '\n'])
            await log_file.write(log)
    