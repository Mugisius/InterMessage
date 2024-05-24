from BotBase import BotBase
from Message import Message, Attachment
import discord


class DiscordBot(BotBase):
    def __init__(self, parameters):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        self.channel = parameters["channel"]
        self.token = parameters['token']
    
        @self.client.event
        async def on_message(message):
            self.base_message_handler(message)

        print("Created DiscordBot")
        
    async def start(self):
        while True:
            await self.client.start(self.token)
    
    def base_message_handler(self, message):
        if message.author == self.client.user:
            return
        if message.channel.id == self.channel:
            attachments = []
            for a in message.attachments:
                attachments.append(Attachment(a.content_type, a.url))
            msg = Message(message.author.name,
                          message.created_at,
                          text=message.content,
                          attachments=attachments)
            self.outcoming.put_nowait(msg)

    async def send(self, message):
        await self.channel.send(message)
    