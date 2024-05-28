import requests

class Message():
    def __init__(self, source, author, date, * , text='', attachments=[]) -> None:
        print(source, author, date, text, attachments)
        self.source = source
        self.author = author
        self.date = date
        self.prefix = f"{author} from {source}: "
        self.text = text
        self.attachments = attachments

class Attachment():
    def __init__(self, type, url=None, file=None, filename=None) -> None:
        self.type = type
        self.url = url
        if not file:
            self.file = requests.get(url).content
        else: 
            self.file = file
        if not filename:
            self.filename = ".".join(type.split("/"))
        else:
            self.filename=filename
