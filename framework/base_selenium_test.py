# Inherit into anything you want from BaseTest to get all of your attributes set as properties on your unittest.TestCase
# EXAMPLE SELENIUM BASE CLASS
import random
from pathlib import Path

import pyautogui
from selenium.webdriver.remote.webdriver import WebDriver

from framework.base_test import BaseTest
from framework.configuration import TestRun
from helpers.file_helper import FileHelper
from helpers.logging import Logger
from test_rail.api_helper import TestRailApi


class BaseSeleniumTest(BaseTest):
    """ This is the base class that should be inherited in all test
    classes that are run as a part of CI/CD.  The BaseTest class inherits
    from unittest.TestCase, so all child classes will have access to the
    unittest architecture.  The inheritance automatically does the following:
    - Sets up logging
    - Will update the test case result in Test Rail with the log file and result if test rail is enabled
    - Tears down driver (quit/close)
    - Saves screenshot
    """

    __platform = object  # DEFAULT
    @property
    def sauce_platform(self) -> dict:
        self.__platform.update({'build': TestRun.test_run_name})
        self.__platform.update({'name': self._testMethodName})
        return self.__platform

    @sauce_platform.setter
    def sauce_platform(self, value):
        self.__platform = value

    __driver = object
    @property
    def driver(self) -> WebDriver:
        return self.__driver

    @driver.setter
    def driver(self, value):
        self.__driver = value


    logs = []

    @classmethod
    def setUpClass(cls):


        # mcguyver the logs here to work with multithreaded functional_tests
        # log_name, log_path = Logger.logging_setup(str(random.randint(9, 99999)))
        # cls.logs.append(Log(log_name, log_path))

        """On inherited classes, run our `setUp` method"""
        if cls is not BaseSeleniumTest and cls.setUp is not BaseSeleniumTest.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                BaseSeleniumTest.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def setUp(self):
        pass

    def tearDown(self):
        print("Test script: " + self._testMethodName +
              " is complete. See script logs for additional details.")

        # get the test case id decorator and log it
        errors_result_log = ''
        failures_result_log = ''
        # get the actual test outcome
        result = self.defaultTestResult()  # these 2 methods have no side effects
        self._feedErrorsToResult(result, self._outcome.errors)

        error = self._list2reason(result.errors)
        failure = self._list2reason(result.failures)
        if error:
            errors_result_log = self._get_all_test_method_exceptions_result_text(error)
        if failure:
            failures_result_log = self._get_all_test_method_failures_result_text(failure)

        # status: [1= passed, 2= blocked,  4= retest, 5= failed ]
        screen_shot_text = self._testMethodName + str(random.randint(9, 99999))
        screen_shot = FileHelper.resolveAgnosticPath(TestRun.screenshots_unc_path, screen_shot_text + '.png')
        # str.format(
        #     r'{}\{}.png', TestRun.screenshots_unc_path, screen_shot_text)
        try:
            self.driver.save_screenshot(str(screen_shot))
        except:
            print('There may have been an issue with taking the screenshot')

        # job_url = ''
        # if TestRun.use_sauce_labs == True:
        #     sauce_status = True
        #     if failure:
        #         sauce_status = False
        #     if error:
        #         sauce_status = False
        #     try:
        #         self.sauce = SauceClient(SauceLabs.user, SauceLabs.access_key)
        #         self.sauce.jobs.update_job(self.driver.session_id, passed=sauce_status)
        #         job = self.sauce.jobs.get_job(self.driver.session_id)
        #         import hmac
        #         from hashlib import md5
        #         a = hmac.new(
        #             bytes("{}:{}".format(
        #                 SauceLabs.user,
        #                 SauceLabs.access_key),
        #                 'latin-1'),
        #             bytes(job['id'], 'latin-1'),
        #             md5)
        #
        #         auth_token = a.hexdigest()
        #         video_url = 'https://assets.saucelabs.com/jobs/{}/video.mp4?auth={}'.format(job['id'], auth_token)
        #         # video_name = job['id'] + '.mp4'
        #         # video_path = FileHelper.resolveAgnosticPath(TestRun.screenshots_unc_path, video_name)
        #         #
        #         # try:
        #         #     import urllib.request
        #         #     urllib.request.urlretrieve(video_url, video_path)
        #         # except:
        #         #     pass
        #
        #         job_url = '[CLICK TO VIEW VIDEO]({})'.format(video_url)
        #
        #         # job_url = '<script src = "https://saucelabs.com/video-embed/{}.js?auth={}"></script>'.format(
        #         #     job['id'],
        #         #     str(auth_token)
        #         # )
        #
        #         #                 # Logger.log_and_debug(99, 'info', str(assets))
        #     except Exception as e:
        #         print('SAUCE EXCEPTION: ' + str(e))
        #         pass

        if TestRun.toggle_test_rail == True:
            test_rail = TestRailApi()
            status = 1
            if failure:
                Logger.log_exception(failure)
                status = 5
            elif error:
                Logger.log_exception(error)
                status = 4
            file = ''

            try:
                file = open(Logger.current_log_file)

            except:
                print('unable to open log file!\nLOG FILE: ' + Logger.current_log_file)

            with file as f:
                print('adding test result')
                result_comment = '\n'.join(
                    f.readlines()) + self.get_screen_shot_log_text(screen_shot_text)
                current_test_results = []
                for line in result_comment.split('\n'):
                    # test logs
                    if line.__contains__(self._testMethodName):
                        if line == self._get_exception_identifier():
                            continue
                        current_test_results.append(line)
                result = '\n'.join(current_test_results)
                result = result + errors_result_log
                result = result + failures_result_log

                # if TestRun.use_sauce_labs == True:
                #     result = result + '\n\n#' + job_url + '#\n\n'


                # This assumes since you have test rail toggled - you've created a test run
                test_case_id = self.test_case_id
                if test_case_id is None:
                    test_case_id = test_rail.get_test_id_by_title(
                        self._testMethodName, self.test_type.test_section_id)

                try:
                    test_rail.add_test_case_result_for_test_run(
                        TestRun.test_run_id, test_case_id, status, str(result))
                except:
                    test_case_id = test_rail.get_test_id_by_title(
                        self._testMethodName, self.test_type.test_section_id)

                    test_rail.add_test_case_result_for_test_run(
                        TestRun.test_run_id, test_case_id, status, str(result))

        try:
            self.driver.close()
            self.driver.quit()
        except:
            print(
                'there may have been an issue closing or quitting the driver.  Killing all driver processes')


    @staticmethod
    def get_screen_shot_log_text(log_name):
        my_file = Path(str.format(r'{}\{}.png', TestRun.screenshots_unc_path, log_name))
        if my_file.is_file():
            return '\n\nSCREENSHOT ----->\n ![View Screenshot](' + str.format(
                '{}/{}.png', TestRun.screenshots_test_rail_virtual_directory, log_name) + ')'

        else:
            # Take screenshot
            pic = pyautogui.screenshot()

            # Save the image
            pic.save(FileHelper.resolveAgnosticPath(TestRun.screenshots_unc_path, log_name + '.png'))
            return '\n\nSCREENSHOT ----->\n ![View Screenshot](' + str.format(
                '{}/{}.png', TestRun.screenshots_test_rail_virtual_directory, log_name) + ')'

    def _get_exception_identifier(self):
        identifier = '{} exceptions ====================>\n'.format(self._testMethodName)
        return identifier

    def _get_failure_identifier(self):
        identifier = '{} failures ====================>\n'.format(self._testMethodName)
        return identifier

    def _get_all_test_method_failures_result_text(self, failures):
        header = '\n\nTHERE WERE FAILURES IN THE TEST!!!!!\n\n'
        id = self._get_exception_identifier()
        text = header + id + failures + id
        return text

    def _get_all_test_method_exceptions_result_text(self, errors):
        header = '\n\nTHERE WERE EXCEPTIONS IN THE TEST!!!!!\n\n'
        id = self._get_exception_identifier()
        text = header + id + errors + id
        return text

    def _list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]


class Log:
    def __init__(self, log: str, log_path: str):
        self.log_name = log
        self.log_path = log_path
