"""Bot for VK app."""
from .BotBase import BotBase
from vkbottle.bot import Bot
from vkbottle import API
from vkbottle import PhotoMessageUploader, AudioUploader, VideoUploader

from ..Message import Message, Attachment

import datetime


class VkBot(BotBase):
    """Bot for VK app."""

    def __init__(self, parameters):
        """Set up VK API client and message handlers."""
        self.token = parameters['token']
        self.peer_id = parameters["channel"]

        self.api = API(token=self.token)
        self.bot = Bot(api=self.api)
        self.photo_uploader = PhotoMessageUploader(self.api)
        self.audio_uploader = AudioUploader(self.api)
        self.video_uploader = VideoUploader(self.api)

        @self.bot.on.message()
        async def on_message(msg):
            """Recive a message from channel and handle it."""
            await self.base_message_handler(msg)

        print(_("Created VkBot"))

    async def start(self):
        """Start client."""
        await self.bot.run_polling()

    def get_attachments(self, msg):
        """
        Get attachments of the message.

        :param msg: message
        """
        attachments = []
        for a in msg.attachments:
            if a.photo:
                url = a.photo.sizes[-5].url
                content_type = "image"
            elif a.video:
                url = a.video.url
                content_type = "video"
            elif a.audio:
                url = a.audio.url
                content_type = "audio"

            attachments.append(Attachment(content_type, url))

        return attachments

    async def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """
        if msg.peer_id != self.peer_id:
            return

        attachments = []  # self.get_attachments(msg)

        msg_user = await self.bot.api.users.get(msg.from_id)
        message = Message("vk",
                          f"{msg_user[0].first_name} {msg_user[0].last_name}",
                          datetime.date(1, 1, 1),
                          text=msg.text,
                          attachments=attachments)

        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.

        :param message: message to send
        """
        if message.text:
            await self.api.messages.send(random_id=0,
                                         peer_id=self.peer_id,
                                         message=message.prefix + message.text)

        for a in message.attachments:
            if (a.type).startswith("image"):
                file = await self.photo_uploader.upload(a.file, peer_id=self.peer_id)
            elif (a.type).startswith("audio"):
                file = await self.audio_uploader.upload(a.file, peer_id=self.peer_id)
            elif (a.type).startswith("video"):
                file = await self.video_uploader.upload(a.file, peer_id=self.peer_id)

            await self.api.messages.send(random_id=0,
                                         peer_id=self.peer_id,
                                         message=message.prefix,
                                         attachment=file)
