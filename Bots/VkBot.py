"""Bot for VK app."""
from Bots.BotBase import BotBase
from _i18n import _
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

        self.api = API(token=self.token)
        self.bot = Bot(api=self.api)

        @self.bot.on.message()
        async def on_message(msg):
            """Recive a message from channel and handle it."""
            await self.base_message_handler(msg)

        print(_("Created VkBot"))

    async def start(self):
        """Start client."""
        await self.bot.run_polling()

    def get_attachments(self):
        return []


    async def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """

        if msg.peer_id != self.peer_id:
            return

        msg_user = await self.bot.api.users.get(msg.from_id)
        message = Message("vk", 
            f"{msg_user[0].first_name} {msg_user[0].last_name}",
            datetime.date(1, 1, 1),
            text=msg.text,
            attachments=[])
        
        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.
        
        :param message: message to send
        """
        if message.text:
            await self.api.messages.send(random_id = 0, 
                                        peer_id=self.peer_id, 
                                        message=message.prefix + message.text) 
