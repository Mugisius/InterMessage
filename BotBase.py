
from abc import ABC, abstractmethod


class BotBase(ABC):

    @abstractmethod
    def __init__():
        print("BotBase abstract method is not implemented")

    @abstractmethod
    def base_message_handler():
        print("BotBase abstract method is not implemented")

    @abstractmethod
    def send():
        print("BotBase abstract method is not implemented")

    def set_queues(self, incoming, outcoming):
        self.incoming = incoming 
        self.outcoming = outcoming