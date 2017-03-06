#!/usr/bin/env python3.5

import os.path
import sharkan
import tempfile
import unittest
import unittest.mock

class SharkanTest(unittest.TestCase):

  def setUp(self):
    self.file = tempfile.mkstemp()[1]
    self.pyed = sharkan.PyEd()

  def test_write_read_read(self):
    self.pyed.write_to_file(self.file, "test text")
    txt = self.pyed.read_file(self.file)
    self.assertEqual(txt, "test text")

  @unittest.mock.patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='test')
  def test_read_file_mock(self, m):
    txt = self.pyed.read_file("mock")
    self.assertEqual(txt, 'test')

  def tearDown(self):
    if os.path.exists(self.file):
      os.remove(self.file)

if __name__ == '__main__':
  unittest.main()
