"""Abstract class for all bots."""
from abc import ABC, abstractmethod
from _i18n import _


class BotBase(ABC):
    """Abstract class for all bots."""

    @abstractmethod
    def __init__():
        """Set up a bot."""
        print(_("BotBase abstract method is not implemented"))

    @abstractmethod
    def base_message_handler(msg):
        """
        Parse a message from chat and create an :class:`Message` object.

        :param message: msg to handle
        """
        print(_("BotBase abstract method is not implemented"))

    @abstractmethod
    async def send(message):
        """
        Send a message to a chat.

        :param message: message to send
        """
        print(_("BotBase abstract method is not implemented"))

    @abstractmethod
    async def start():
        """Start client."""
        print(_("BotBase abstract method is not implemented"))

    def set_queues(self, incoming, outcoming):
        """Set up incoming and outcoming queues."""
        self.incoming = incoming
        self.outcoming = outcoming
