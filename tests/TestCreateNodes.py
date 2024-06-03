import unittest
import yaml
import os
import sys
import aiogram
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from InterMessage.InterMessage import create_nodes_by_conf
import InterMessage

class TestCreateNodes(unittest.TestCase):

    def check_nodes(self, conf, nodes):
        i = 0
        for messenger in conf.values():
            if messenger['name'] == "logger":
                continue
            
            self.assertEqual(nodes[i].bot.token, messenger['parameters']['token'])
            if messenger['name'] == "telegram":
                self.assertEqual(nodes[i].bot.chat_id, messenger['parameters']['channel'])
            elif messenger['name'] == "vk":
                self.assertEqual(nodes[i].bot.peer_id, messenger['parameters']['channel'])
            elif messenger['name'] == "discord":
                self.assertEqual(nodes[i].bot.channel, messenger['parameters']['channel'])
            i+=1

    def check_loops(self, conf, loops):
        self.assertEqual(len(loops), len(conf.values()))
        for loop in loops:
            self.assertIsInstance(loop, types.CoroutineType)

    def test_conf1(self):
        conf1_file_path = "tests/confs_for_create/conf1.yaml"
        file = open(conf1_file_path)
        conf1 = yaml.load(file , Loader=yaml.loader.SafeLoader)
        self.assertRaisesRegex(aiogram.utils.exceptions.ValidationError, "Token is invalid!", create_nodes_by_conf, conf1_file_path)

        file.close()

    def test_conf2(self):
        conf2_file_path = "tests/confs_for_create/conf2.yaml"
        file = open(conf2_file_path)
        conf2 = yaml.load(file , Loader=yaml.loader.SafeLoader)
        nodes, loops = create_nodes_by_conf(conf2_file_path)
        
        self.check_nodes(conf2, nodes)
        self.check_loops(conf2, loops)

        file.close()
       
if __name__ == "__main__":
    unittest.main()