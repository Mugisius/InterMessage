import unittest
import yaml
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from InterMessage.InterMessage import validate

def nothing(smth):
    return smth

import builtins
builtins.__dict__['_']=nothing

class TestValidate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/confs_for_validate/conf1.yaml") as file:
            cls.conf1 = yaml.load(file, Loader=yaml.loader.SafeLoader)
        with open("tests/confs_for_validate/conf2.yaml") as file:
            cls.conf2 = yaml.load(file, Loader=yaml.loader.SafeLoader)
        with open("tests/confs_for_validate/conf3.yaml") as file:
            cls.conf3 = yaml.load(file, Loader=yaml.loader.SafeLoader)
        with open("tests/confs_for_validate/conf4.yaml") as file:
            cls.conf4 = yaml.load(file, Loader=yaml.loader.SafeLoader)
        with open("tests/confs_for_validate/conf5.yaml") as file:
            cls.conf5 = yaml.load(file, Loader=yaml.loader.SafeLoader)

    def test_conf1(self):
        self.assertEqual(validate(TestValidate.conf1), True)

    def test_conf2(self):
        self.assertEqual(validate(TestValidate.conf2), False)

    def test_conf3(self):
        self.assertEqual(validate(TestValidate.conf3), False)

    def test_conf4(self):
        self.assertEqual(validate(TestValidate.conf4), False)

    def test_conf5(self):
        self.assertEqual(validate(TestValidate.conf5), False)


if __name__ == "__main__":
    unittest.main()
