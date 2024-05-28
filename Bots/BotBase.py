
from abc import ABC, abstractmethod


class BotBase(ABC):

    @abstractmethod
    def __init__():
        print("BotBase abstract method is not implemented")

    @abstractmethod
    def base_message_handler():
        print("BotBase abstract method is not implemented")

    @abstractmethod
    async def send():
        print("BotBase abstract method is not implemented")

    @abstractmethod
    async def start():
        print("BotBase abstract method is not implemented")

    @abstractmethod
    def get_attachments(msg):
        print("BotBase abstract method is not implemented")

    def set_queues(self, incoming, outcoming):
        self.incoming = incoming 
        self.outcoming = outcoming