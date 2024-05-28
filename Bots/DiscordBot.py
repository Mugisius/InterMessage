"""Bot for Discord app."""
from Bots.BotBase import BotBase
from Message import Message, Attachment
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

    def base_message_handler(self, msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """
        if msg.author == self.client.user:
            return

        attachments = []
        for a in msg.attachments:
            attachments.append(Attachment(a.content_type, a.url))

        message = Message(msg.author.name,
                          msg.created_at,
                          text=msg.content,
                          attachments=attachments)
        message.source = "discord"

        self.outcoming.put_nowait(message)

    async def send(self, message):
        """
        Send a message to a chat.

        :param message: message to send
        """
        await self.channel.send(message.text)
