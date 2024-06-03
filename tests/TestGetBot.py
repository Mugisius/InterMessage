import unittest
import yaml
import os
import sys
import aiogram
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from InterMessage.InterMessage import get_bot
import InterMessage

class TestGetBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conf_file_path = "tests/confs_for_create/conf2.yaml"
        file = open(conf_file_path)
        cls.conf = yaml.load(file , Loader=yaml.loader.SafeLoader)

        file.close()

    def test_get_vk(self):
        parameters = TestGetBot.conf['VkBot']['parameters']
        self.assertIsInstance(get_bot("vk", parameters), InterMessage.Bots.VkBot.VkBot)

    def test_get_discord(self):
        parameters = TestGetBot.conf['DiscordBot']['parameters']
        self.assertIsInstance(get_bot("discord", parameters), InterMessage.Bots.DiscordBot.DiscordBot)

    def test_get_telegram(self):
        parameters = TestGetBot.conf['TelegramBot']['parameters']
        self.assertIsInstance(get_bot("telegram", parameters), InterMessage.Bots.TelegramBot.TelegramBot)
       
if __name__ == "__main__":
    unittest.main()