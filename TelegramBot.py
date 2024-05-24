from BotBase import BotBase
import asyncio
import aiogram

class TelegramBot(BotBase):
    
    def __init__(self, parameters):
        self.token = parameters['token']
        self.chat_id = parameters["channel"]

        self.bot = aiogram.Bot(token=self.token)
        self.dp = aiogram.Dispatcher()

        @self.dp.message()
        async def on_message(message):
            self.base_message_handler(message)

        print("Created TelegramBot")

    async def start(self):
        
        self.bot_user = await self.bot.get_me()
        await self.dp.start_polling(self.bot)

    def base_message_handler(self, message):
        print("Id чата:", message.from_user.id)
        if message.from_user == self.bot_user:
            return
        self.outcoming.put_nowait(message)

    async def send(self, message):
        text = message
        await self.bot.send_message(self.chat_id, text) 



        
