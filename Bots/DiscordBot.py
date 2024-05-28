from Bots.BotBase import BotBase
from Message import Message, Attachment
import discord


class DiscordBot(BotBase):
    def __init__(self, parameters):
        intents = discord.Intents.all()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.channelID = parameters['channel']

        self.token = parameters['token']
    
        @self.client.event
        async def on_ready():
            self.channel = await self.client.fetch_channel(self.channelID)

        @self.client.event
        async def on_message(message):
            self.base_message_handler(message)

        print("Created DiscordBot")
        
    async def start(self):
        await self.client.start(self.token)

    def get_attachments(self, msg):
        attachments = []
        for a in msg.attachments:
            attachments.append(Attachment(a.content_type, a.url))
        
        return attachments
    
    def base_message_handler(self, msg):
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

        if message.text:
            b=0
            await self.channel.send(message.prefix + message.text)

        for a in message.attachments:
            b=0
            await self.channel.send(message.prefix, file=discord.File(a.file, filename=a.filename))
    