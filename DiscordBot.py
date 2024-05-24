from BotBase import BotBase
import discord


class DiscordBot(BotBase):
    def __init__(self, parameters):
        intents = discord.Intents.all()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        self.token = parameters['token']
    
        @self.client.event
        async def on_message(message):
            self.base_message_handler(message)

        print("Created DiscordBot")
        
    async def start(self):
        await self.client.start(self.token)
    
    def base_message_handler(self, message):
        print("Id чата:", message.channel.id)
        self.channel = self.client.get_channel(message.channel.id)
        print(self.channel)
        if message.author == self.client.user:
            return
        print("Message content is", message.content)
        self.outcoming.put_nowait(message.content)

    async def send(self, message):
        print("Message to discord:", message.text)
        await self.channel.send(message.text)
    