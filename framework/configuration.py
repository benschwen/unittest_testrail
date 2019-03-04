class TestRun:
    """ Configuration for  all test runs - values are usually populated by test_controller.py"""
    # configuration for test runs here
    project_id = 3
    selenium_timeout = 120 # 2 minutes when finding web elements
    log_file_base_path = ""  # must include the ending "/"
    use_sauce_labs = False
    toggle_test_rail = False
    test_run_name_format = "Run for: ['{}'] {}"
    test_run_name = ''
    test_run_id = ''
    test_type = ''
    server_address = ''
    test_run_case_ids = []
    test_plan_id = 0
    screenshots_unc_path = R''
    screenshots_test_rail_virtual_directory = '/screen_shots'
    concurrent_tests = 4 # see test_controller.py example for a little concurrency fun with your tests

# class SauceLabs:
#     user = ''
#     access_key = ''

class EndPoints:
    """ Configuration for all endpoints based on
            $TEST_ENV environment variable """
    test_rail_url = 'testrail.company.net/testrail'

class Credentials:
    test_rail_user = 'yomama'
    test_rail_password = 'TheRockIsMyfriend22'



