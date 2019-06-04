import unittest

#import backend test modules
from tests import test_pointcloud
from tests import test_cmdarguments
from tests import test_util
from tests import test_file_helper
from tests import test_cadaster_reader

#initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

#add test to the test suite
suite.addTest(loader.loadTestsFromModule(test_pointcloud))
suite.addTest(loader.loadTestsFromModule(test_cmdarguments))
suite.addTest(loader.loadTestsFromModule(test_util))
suite.addTest(loader.loadTestsFromModule(test_file_helper))
suite.addTest(loader.loadTestsFromModule(test_cadaster_reader))
#initialize a runner, pass it your suit and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)