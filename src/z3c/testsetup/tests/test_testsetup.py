import os
import sys
import gc
import re
import unittest
from zope.testing import doctest, cleanup, renormalizing
import zope.component.eventtesting
from z3c.testsetup.util import get_package

TESTFILES = ['basicsetup.txt', 'functionaldoctestsetup.txt',
             'pythontestsetup.txt', 'unitdoctestsetup.txt', 'util.txt',
             'unittestsetup.txt']

def pnorm(path):
    """Normalization of paths to use forward slashes. This is needed
    to make sure the tests work on windows.
    """
    return path.replace(os.sep, '/')

def get_testcases_from_suite(suite):
    result=[]
    for elem in list(suite):
        if isinstance(elem, unittest.TestCase):
            result.append(elem)
        if isinstance(elem, unittest.TestSuite):
            result.extend(
                get_testcases_from_suite(elem))
    return result


def get_filenames_from_suite(suite):
    testcases = get_testcases_from_suite(suite)
    result = []
    for testcase in testcases:
        filename = str(testcase)
        if ' ' in filename:
            filename = str(get_package(testcase.__module__).__file__)
            filename = os.path.splitext(filename)[0] + '.py'
        result.append(filename)
    result.sort()
    return result

def get_basenames_from_suite(suite):
    basenames = [os.path.basename(x) for x in get_filenames_from_suite(suite)]
    basenames.sort()
    return basenames
    

def setUpZope(test):
    zope.component.eventtesting.setUp(test)

def cleanUpZope(test):
    cleanup.cleanUp()

checker = renormalizing.RENormalizing([
    # str(Exception) has changed from Python 2.4 to 2.5 (due to
    # Exception now being a new-style class).  This changes the way
    # exceptions appear in traceback printouts.
    (re.compile(r"ConfigurationExecutionError: <class '([\w.]+)'>:"),
                r'ConfigurationExecutionError: \1:'),
    ])

def testrunner_suite():
    def setUp(test):
        test.globs['saved-sys-info'] = (
            sys.path[:],
            sys.argv[:],
            sys.modules.copy(),
            gc.get_threshold(),
            )
        test.globs['this_directory'] = os.path.split(__file__)[0]
        test.globs['testrunner_script'] = __file__
        test.globs['get_basenames_from_suite'] = get_basenames_from_suite

    def tearDown(test):
        sys.path[:], sys.argv[:] = test.globs['saved-sys-info'][:2]
        gc.set_threshold(*test.globs['saved-sys-info'][3])
        sys.modules.clear()
        sys.modules.update(test.globs['saved-sys-info'][2])
    suites = [
        doctest.DocFileSuite(
        'testrunner.txt', 'README.txt', 'testgetter.txt',
        package='z3c.testsetup',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
        checker=checker),
        ]

    suite = unittest.TestSuite(suites)
    return suite


def suiteFromFile(filename):
    suite = unittest.TestSuite()
    test = doctest.DocFileSuite(filename,
                                package = 'z3c.testsetup',
                                setUp=setUpZope,
                                tearDown=cleanUpZope,
                                globs={'pnorm':pnorm,
                                       'get_basenames_from_suite':
                                       get_basenames_from_suite},
                                checker=checker,
                                optionflags=doctest.ELLIPSIS+
                                doctest.NORMALIZE_WHITESPACE)

    suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in TESTFILES:
        suite.addTest(suiteFromFile(name))
    suite.addTest(testrunner_suite())
    return suite
