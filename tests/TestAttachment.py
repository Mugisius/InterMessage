import unittest
import yaml
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from InterMessage.Message import Attachment

def nothing(smth):
    return smth

import builtins
builtins.__dict__['_']=nothing

class TestCreateNodes(unittest.TestCase):

    def test_a_only_type(self):
        a = Attachment("image/jpeg")
        self.assertIsNone(a.file)
        self.assertEqual(a.filename, "image.jpeg")

    def test_a_by_url(self):
        a = Attachment("image/jpeg", url="https://google.com")
        self.assertIsNotNone(a.file)
        self.assertEqual(a.filename, "image.jpeg")

    def test_a_by_file(self):
        file = 5
        a = Attachment("image/jpeg", file=file)
        self.assertEqual(a.file, file)
        self.assertEqual(a.filename, "image.jpeg")

    def test_a_filename(self):
        filename = "filename"
        a = Attachment("image/jpeg", filename=filename)
        self.assertIsNone(a.file)
        self.assertEqual(a.filename, filename)


if __name__ == "__main__":
    unittest.main()
