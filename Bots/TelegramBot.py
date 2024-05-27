"""Bot for Telegram app."""
from Bots.BotBase import BotBase
from Message import Message, Attachment
import aiogram
import logging


logging.basicConfig(level=logging.ERROR)


class TelegramBot(BotBase):
    """Bot for Telegram app."""

    def __init__(self, parameters):
        """Set up telegram bot client and message handlers."""
        self.token = parameters['token']
        self.chat_id = parameters["channel"]

        self.bot = aiogram.Bot(token=self.token)
        self.dp = aiogram.Dispatcher(self.bot)

        @self.dp.message_handler()
        async def on_message(message):
            """Recive a message from channel and handle it."""
            self.base_message_handler(message)

        print("Created TelegramBot")

    async def start(self):
        """Start client."""
        self.bot_user = await self.bot.get_me()
        await self.dp.start_polling(self.bot)

    def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """
        if msg.from_user == self.bot_user or msg.chat.id != self.chat_id:
            return

        message = Message(msg.from_user.first_name,
                          msg.date,
                          text=msg.text,
                          attachments=[])
        message.source = "telegram"

        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.

        :param message: message to send
        """
        await self.bot.send_message(self.chat_id, message.text)
