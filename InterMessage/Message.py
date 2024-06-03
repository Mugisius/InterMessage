"""Message and Attachment classes."""
import requests


class Message():
    """Message class."""

    def __init__(self, source, author, date, *, text='', attachments=[]) -> None:
        """Set up source, author, date, text and attachments of message."""
        self.source = source
        self.author = author
        self.date = date
        self.prefix = _("{} from {}: ").format(author, source)
        self.text = text
        self.attachments = attachments


class Attachment():
    """Attachment class."""

    def __init__(self, type, url=None, file=None, filename=None) -> None:
        """Set up type, url, filename of message and save it in memory."""
        self.type = type
        self.url = url
        if not file:
            self.file = requests.get(url).content
        else:
            self.file = file
        if not filename:
            self.filename = ".".join(type.split("/"))
        else:
            self.filename = filename
