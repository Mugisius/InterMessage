import requests

class Message():
    def __init__(self, author, date, * , text='', attachments=[]) -> None:
        self.author = author
        self.date = date
        self.text = text
        self.attachments = attachments

class Attachment():
    def __init__(self, type, url) -> None:
        self.type = type
        self.url = url
        self.file = requests.get(url).content
