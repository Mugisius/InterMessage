"""Bot for VK app."""
from Bots.BotBase import BotBase
from vkbottle.bot import Bot
from vkbottle import API

from Message import Message, Attachment

import datetime

class VkBot(BotBase):
    """Bot for VK app."""

    def __init__(self, parameters):
        """Set up VK API client and message handlers."""
        self.token = parameters['token']
        self.peer_id = parameters["channel"]

        print(self.token)
        self.api = API(token=self.token)
        self.bot = Bot(api=self.api)


        @self.bot.on.message()
        async def on_message(msg):
            """Recive a message from channel and handle it."""
            self.base_message_handler(msg)

        print("Created VkBot")

    async def start(self):
        """Start client."""
        await self.bot.run_polling()

    def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.
        
        :param message: msg to handle
        """
        print("Chat ID:", msg.chat_id)
        print("Peer ID:", msg.peer_id)
        print("From Id:", msg.from_id)
        if msg.peer_id != self.peer_id:
            return

        message = Message(str(msg.from_id),
              datetime.date(1, 1, 1),
              text=msg.text,
              attachments=[])
        
        message.source = "vk"
        
        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.
        
        :param message: message to send
        """
        await self.api.messages.send(random_id=0, peer_id=self.peer_id, message=message.text)
