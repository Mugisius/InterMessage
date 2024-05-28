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

        @self.dp.message_handler(content_types=["photo", "text", "audio", "video"])
        async def on_message(message):
            """Recive a message from channel and handle it."""
            await self.base_message_handler(message)

        print(_("Created TelegramBot"))

    async def start(self):
        """Start client."""
        self.bot_user = await self.bot.get_me()
        await self.dp.start_polling(self.bot)

    async def get_attachment_file(self, attach_object):
        """
        Get the file from attachment object.

        :param attach_object: attachment object
        """
        file_stream = await self.bot.get_file(attach_object['file_id'])
        file = await self.bot.download_file(file_stream.file_path)
        return file

    async def get_attachments(self, msg):
        """
        Get attachments of the message.

        :param msg: message
        """
        attachments = []
        if msg.photo:
            photo = msg.photo[-1]
            file = await self.get_attachment_file(photo)
            attachments.append(Attachment(type='image/jpeg', file=file))
        elif msg.video:
            video = msg.video
            file = await self.get_attachment_file(video)
            attachments.append(Attachment(type='video/mp4', file=file))
        elif msg.audio:
            audio = msg.audio
            file = await self.get_attachment_file(audio)
            attachments.append(Attachment(type='audio/mp3', file=file))

        return attachments

    async def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """
        if msg.from_user == self.bot_user or msg.chat.id != self.chat_id:
            return

        attachments = await self.get_attachments(msg)
        message = Message("telegram",
                          msg.from_user.first_name,
                          msg.date,
                          text=msg.text,
                          attachments=attachments)

        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.

        :param message: message to send
        """
        if message.text:
            await self.bot.send_message(self.chat_id, message.prefix + message.text)

        for a in message.attachments:
            if (a.type).startswith("image"):
                await self.bot.send_photo(self.chat_id, a.file, caption=message.prefix)
            elif (a.type).startswith("audio"):
                await self.bot.send_audio(self.chat_id, a.file, caption=message.prefix)
            elif (a.type).startswith("video"):
                await self.bot.send_video(self.chat_id, a.file, caption=message.prefix)
