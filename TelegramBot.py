from BotBase import BotBase
from Message import Message, Attachment
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

    def base_message_handler(self, msg):

        if msg.from_user == self.bot_user:
            return
        
        message = Message(msg.from_user.first_name,
              msg.date,
              text=msg.text,
              attachments=[])
        message.source = "telegram"
        
        self.outcoming.put_nowait(message)

    async def send(self, message):
        await self.bot.send_message(self.chat_id, message.text) 



        
