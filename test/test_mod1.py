import unittest
from ndl_ocr.util import Util

class TestMod1(unittest.TestCase):
  def test_getFileIdAndName(self):
    self.assertEqual(Util.getFileIdAndName("/tmp/test.txt"), "test")