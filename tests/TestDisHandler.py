import unittest
import yaml
import os
import sys
import asyncio
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from InterMessage.InterMessage import get_bot

class AuthorModel:

    def __init__(self, name=None):
        self.name = name

class MessageModel:
    
    def __init__(self, attachments=[], author=None, created_at=None, content=None):
        self.attachments = attachments
        self.author = author
        self.created_at = created_at
        self.content = content


class TestDisHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conf_file_path = "tests/confs_for_create/conf2.yaml"
        file = open(conf_file_path)
        conf = yaml.load(file , Loader=yaml.loader.SafeLoader)
        parameters = conf['DiscordBot']['parameters']
        cls.dis_bot = get_bot("discord", parameters)

        file.close()

    def test_smoke(self):
        outcoming = asyncio.Queue()
        incoming = asyncio.Queue()
        TestDisHandler.dis_bot.set_queues(outcoming, incoming)

        msg = MessageModel(author=AuthorModel("Nowhere man"), created_at=datetime.datetime(1, 1, 1), content="Nowhere text")

        TestDisHandler.dis_bot.base_message_handler(msg)

        message = TestDisHandler.dis_bot.outcoming.get_nowait()

        self.assertEqual(message.source, "discord")
        self.assertEqual(message.author, "Nowhere man")
        self.assertEqual(message.date, datetime.datetime(1, 1, 1))
        self.assertEqual(message.prefix, "Nowhere man from discord: ")
        self.assertEqual(message.text, "Nowhere text")
        self.assertEqual(message.attachments, [])
        

if __name__ == "__main__":
    unittest.main()