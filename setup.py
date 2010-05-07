from setuptools import setup, find_packages
import imp
mod = imp.load_source('tracreportmail_test', './test/tracreportmail_test.py')

setup(
    name = "TracReportMail",
    version = "0.1",
    packages = find_packages(),
    test_suite = 'tracreportmail_test.suite'
)
