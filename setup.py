from setuptools import setup, find_packages
import sys
sys.path.append('./src')
sys.path.append('./test')

setup(
    name = "TracReportMail",
    version = "0.1",
    packages = find_packages(),
    test_suite = 'tracreportmail_test.suite'
)
