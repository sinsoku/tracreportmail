#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest
import tracreportmail as trm

class TestSample(unittest.TestCase):
    def testsample(self):
        self.assert_(trm.send)

def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TestSample))
  return suite

if __name__ == '__main__':
    unittest.main()
