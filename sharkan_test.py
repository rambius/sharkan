#!/usr/bin/env python3.5

import os.path
import sharkan
import tempfile
import unittest

class SharkanTest(unittest.TestCase):

  def setUp(self):
    self.file = tempfile.mkstemp()[1]

  def test_write_read(self):
    pyed = sharkan.PyEd()
    pyed.write_to_file(self.file, "test text")
    txt = pyed.read_file(self.file)
    self.assertEqual(txt, "test text")

  def tearDown(self):
    if os.path.exists(self.file):
      os.remove(self.file)

if __name__ == '__main__':
  unittest.main()
