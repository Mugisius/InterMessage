"""Message and Attachment classes."""
import requests


class Message():
    """Message class."""

    def __init__(self, author, date, *, text='', attachments=[]) -> None:
        """Set up author, date, text and attachments of message."""
        self.author = author
        self.date = date
        self.text = text
        self.attachments = attachments


class Attachment():
    """Attachment class."""

    def __init__(self, type, url) -> None:
        """Set up type, url of message and save it in memory."""
        self.type = type
        self.url = url
        self.file = requests.get(url).content
