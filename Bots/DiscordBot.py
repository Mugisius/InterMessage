"""Bot for Discord app."""
from Bots.BotBase import BotBase
from Message import Message, Attachment
from _i18n import _
import discord


class DiscordBot(BotBase):
    """Bot for Discord app."""

    def __init__(self, parameters):
        """Set up discord API client and message handlers."""
        intents = discord.Intents.all()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.channelID = parameters['channel']

        self.token = parameters['token']

        @self.client.event
        async def on_ready():
            """Get channel for operate."""
            self.channel = await self.client.fetch_channel(self.channelID)

        @self.client.event
        async def on_message(message):
            """Recive a message from channel and handle it."""
            self.base_message_handler(message)

        print(_("Created DiscordBot"))

    async def start(self):
        """Start client."""
        await self.client.start(self.token)


    def get_attachments(self, msg):
        attachments = []
        for a in msg.attachments:
            attachments.append(Attachment(a.content_type, a.url))
        
        return attachments
    
    def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """
        if msg.author == self.client.user:
            return
        
        attachments = self.get_attachments(msg)

        message = Message("discord",
            msg.author.name,
            msg.created_at,
            text=msg.content,
            attachments=attachments)
        
        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.

        :param message: message to send
        """
        
        if message.text:
            await self.channel.send(message.prefix + message.text)

        for a in message.attachments:
            await self.channel.send(message.prefix, file=discord.File(a.file, filename=a.filename))
    
