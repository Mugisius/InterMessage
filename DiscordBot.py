from BotBase import BotBase
import discord


class DiscordBot(BotBase):
    def __init__(self, parameters):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.channel = parameters["channel"]
    
        @self.client.event
        async def on_message(message):
            self.base_message_handler(message)
        
        self.loop = self.client.run(parameters['token'])
        print("Created DiscordBot")
    
    def base_message_handler(self, message):
        if message.author == self.client.user:
            return
        if message.channel.id == self.channel:
            print("TRY PUT ", message.content)
            self.outcoming.put_nowait(message.content)

    def send(self, message):
        self.message.channel.send(message)
    