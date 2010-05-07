#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest

class TestSample(unittest.TestCase):
    def testsample(self):
        self.assertTrue(True)

def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TestSample))
  return suite

if __name__ == '__main__':
    unittest.main()
