# EXAMPLE FILE!!!!!!!!!!!

# SEE END OF FILE TO SEE HOW IT'S BEING USED!!!!!


import argparse
import unittest
import sys

# from functional_tests.warehouse_management.dom_tests import SearchOrders_FifthRow
from helpers.logging import Logger
from framework.attributes.categories import Category, UserScenario, Applications, Market
from test_modules.functional.selenium_tests import EcommerceSeleniumTests
from test_modules.integration.api_tests import EcommerceApiTests

sys.path.append('.')
from unittest import TestSuite
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from framework.base_test import BaseSeleniumTest
from framework.configuration import TestRun
from framework.attributes.test_types import TestType
from test_rail.api_helper import TestRailApi

# ADD ARGUMENTS TO FORMULATE YOUR TEST RUN THE WAY YOU'D LIKE
parser = argparse.ArgumentParser(description='Create a Test Run')
parser.add_argument(
    'TEST_TYPE',
    metavar='TEST_TYPE',
    type=str,
    nargs='?',
    help='Known Test Types: FUNCTIONAL | INTEGRATION')
parser.add_argument(
    'SERVER_ADDRESS',
    metavar='SERVER_ADDRESS',
    type=str,
    nargs='?',
    help='Optional.  An address or url to use in the '
         'selenium test run')
parser.add_argument(
    'CATEGORY',
    metavar='CATEGORY',
    type=str,
    nargs='?',
    help='Known Test Categoris: ECOMMERCE | CANADA etc...',
    default=None)

args = parser.parse_args()
__test_type = args.TEST_TYPE
__test_category = args.CATEGORY
if __test_category == 'all':
    __test_category = None
__server_address = args.SERVER_ADDRESS


######### GLOBALS: VERY IMPORTANT FIELD SETTING HERE->
TestRun.test_type = __test_type
TestRun.server_address = __server_address
TestRun.toggle_test_rail = True
TestRun.log_file_base_path = 'test_modules/test_output/script_logs/'  # have to change log file base path when running from test controller
# if server_address == 'stage.env.com' or \
#         server_address == 'stg2.env.com' or \
#         server_address == 'qa2.env.com':
#     TestRun.use_sauce_labs = True
#####################

#### UNITTEST ##############
loader = unittest.TestLoader()
test_suite_by_category = unittest.TestSuite()
#####################

####### LOGGING ##########
dt_string = datetime.now()
log_title = __test_type + '_' + str(dt_string.strftime("%Y%m%d-%H%M%S"))
log_name, log_path = Logger.logging_setup(log_title)
BaseSeleniumTest.logs.append(log_name)
#####################

def _load_tests_of_type(test_class, test_type: TestType, categories=None):
    for name, method in test_class.__dict__.items():
        if hasattr(method, 'test_type'):
            tp = method.test_type
            if tp == test_type:
                if categories is not None:
                    if hasattr(method, 'test_category'):
                        for c in method.test_category:
                            item = [cat for cat in categories if cat.category is c.category]
                            if item.__len__() != 0:
                                test_suite_by_category.addTest(test_class(name))
                else:
                    test_suite_by_category.addTest(test_class(name))


def _run_tests_in_class(test_class):
    """
    # initialize a runner, pass it your suite and run it
    :param test_class: runs all cases from specific class (unittest.TestCase or BaseSeleniumTest)
    :return:
    """
    runner = unittest.TextTestRunner(verbosity=3)
    if test_class.countTestCases() != 0:
        print('************* STARTING TEST RUN *************')
        result = runner.run(test_class)
        print(str(result))
        return result  # this is where we'll return!  We have to have a function here in order to return specifics,
        # so we can determine what unittest tells us about the test run, then return a 1 for no exceptions and a 0
        # for exceptions.
    else:
        print(
            '*****Could not create any test runs from test_controller!' +
            str.format(
                '\n***** Arguments Passed into Script: TEST_TYPE={}, SERVER_ADDRESS={}',
                __test_type, __server_address)
        )
        return 0


def build_test_suite(test_type_param):
    if test_type_param == 'functional':

        # SHOWING AN EXAMPLE OF HOW YOU'D SET A DIFFERENT TEST PLAN FOR EACH ENVIRONMENT'S FUNCTIONAL TESTS
        if TestRun.server_address.__contains__('qa2'):
            TestRun.test_plan_id = '3829'
        if TestRun.server_address.__contains__('qa4'):
            TestRun.test_plan_id = '4699'
        if TestRun.server_address.__contains__('stage') or TestRun.server_address.__contains__('stg2'):
            TestRun.test_plan_id = '3828'
        if TestRun.server_address.__contains__('stg1'):
            TestRun.test_plan_id = '4424'

        if __test_category == 'ECOMMERCE':
            _load_tests_of_type(EcommerceSeleniumTests, TestType.FUNCTIONAL, [Category(Applications.ECOMMERCE)])
        if __test_category == 'ENROLLMENTS':
            _load_tests_of_type(EcommerceSeleniumTests, TestType.FUNCTIONAL, [Category(UserScenario.ENROLLMENT)])
        if __test_category == 'CANADA':
            _load_tests_of_type(EcommerceSeleniumTests, TestType.FUNCTIONAL, [Category(Market.CANADA)])

        if __test_category == None:
            _load_tests_of_type(EcommerceSeleniumTests, TestType.FUNCTIONAL)

    if test_type_param == 'INTEGRATION':
        # SHOWING AN EXAMPLE OF HOW YOU'D SET A DIFFERENT TEST PLAN FOR EACH ENVIRONMENT'S INTEGRATION TESTS

        if TestRun.server_address.__contains__('qa2'):
            TestRun.test_plan_id = '111'
        if TestRun.server_address.__contains__('qa4'):
            TestRun.test_plan_id = '222'
        if TestRun.server_address.__contains__('stage') or TestRun.server_address.__contains__('stg2'):
            TestRun.test_plan_id = '333'
        if TestRun.server_address.__contains__('stg1'):
            TestRun.test_plan_id = '444'

        _load_tests_of_type(EcommerceApiTests, TestType.INTEGRATION)


def initialize_test_rail_test_run():
    TestRun.test_run_name = str.format(
        TestRun.test_run_name_format,
        __server_address,
        dt_string.strftime("%B_%d_%Y|%I:%M%p")
    )

    test_case_ids = []
    test_rail = TestRailApi()
    # Get all the test methods that were loaded from our test class loading above
    for test in test_suite_by_category._tests:
        full_name = str(test)
        full_length = full_name.__len__()

        # This gets the test method name without the class name, etc.
        index = full_name.index(' ', 0, full_length)
        test_method_name = str(test)[0:index]

        if test.test_case_id is None:
            # this will create the test case if no test case exists by that title, if one does, it'll just add it
            test_case_id = test_rail.add_test_case(
                test.test_type.test_section_id, test_method_name, 3)
            test_case_ids.append(test_case_id)
        else:
            test_case_ids.append(test.test_case_id)

    # Need to set global TestRun.test_Run_Id in order to save the results to this test run in the base class
    TestRun.test_run_id = test_rail.create_test_run(
        test_rail.create_test_run_data(
            TestRun.test_run_name, test_case_ids), TestRun.test_plan_id)['id']


def run_tests(suite: TestSuite):
    with ThreadPoolExecutor(max_workers=TestRun.concurrent_tests) as executor:
        list_of_suites = list(suite)
        for test in range(len(list_of_suites)):
            # for item in range(5):
            executor.submit(_run_tests_in_class, list_of_suites[test])


build_test_suite(__test_type)
initialize_test_rail_test_run()
run_tests(test_suite_by_category)
