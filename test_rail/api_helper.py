from framework.configuration import TestRun, EndPoints, Credentials
from test_rail.testrail import *


class TestRailApi:
    """ TestRailApi gives you access to do most of anything you'd like
    with Test Rail.
    Popular use-
    -Get/Create test case
    -Get/Create test run
    -Get/Create test result
    """

    def __init__(self):
        self.client = APIClient(EndPoints.test_rail_url)
        self.client.user = Credentials.test_rail_user
        self.client.password = Credentials.test_rail_password

    project_Id = TestRun.project_id

    # def get_Test_Case_Ids():
    #     return

    def get_sections(self):
        request = str.format('get_sections/{}', self.project_Id)
        return self.client.send_get(request)

    def get_section_id_by_name(self, name):
        all_sections = self.get_sections()
        for section in all_sections:
            if section['name'] == name:
                return section['id']

    def find_test_in_sections(self, testTitle):
        """ Returns secitonId of where test is found, if
        test is not found, returns '' """
        all_sections = self.get_sections()
        for section in all_sections:
            found_test = self.get_test_id_by_title(
                testTitle, section['id'])
            if found_test == '':
                continue
            else:
                return section['id']
        print('test: ' + testTitle + ' not found in project')
        return ''

    def get_run_id(self, testRunName):
        request = str.format('update_runs/{}', self.project_Id)
        print(str(self.client.send_get(request)))

    def update_test_run(self, runId, testRunData):
        request = str.format('update_run/{}', runId)
        response = self.client.send_post(request, testRunData)
        print('Test Run Create Response: ' + str(response))
        return response

    def get_all_test_ids_in_section(self, parentSection, section):
        return self.get_test_cases(
            self.get_test_section_id(
                parentSection, section))

    def get_test_section_id(self, parentSection, section):
        parent_Section_Id = self.get_parent_section_id(parentSection)
        return self.get_section_id(parent_Section_Id, section)

    @staticmethod
    def create_test_case_data(title, testType):
        """test type = [1=acceptance, 3=automated, 9=regression]"""
        data = {'title': title, 'type_id': testType}
        return data

    @staticmethod
    def create_test_run_data(name, testCaseIds):
        """test case ids will be an array i.e. [1,2,3,6]"""
        data = {
            "name": name,
            "include_all": False,
            "case_ids": testCaseIds
        }
        return data

    @staticmethod
    def create_test_plan_data(testRunDatas):
        """test case ids will be an array i.e. [1,2,3,6]"""
        data = {
            "suite_id": '6',
            "name": testRunDatas['name'],
            "include_all": False,
            "case_ids": testRunDatas['case_ids']
            # "runs": [testRunDatas]
        }
        return data

    def get_test_case(self, id):
        request = str.format('get_case/{}', id)
        return self.client.send_get(request)

    def get_test_cases(self, sectionId):
        request = str.format('get_cases/{}&section_id={}', self.project_Id, sectionId)
        return self.client.send_get(request)

    def get_test_id_by_title(self, title, sectionId):
        tests = self.get_test_cases(sectionId)
        for test in tests:
            if test['title'] == title:
                return test['id']
        return ''

    def add_test_case(self, sectionId, title, testType):
        """ *Returns Test Case Id*  Adds a test case to the section.
        If there is already a test with the same title in the section,
        it returns the id of the test case.
        :testType = [1=acceptance, 3=automated, 9=regression]"""
        test_case_id = self.get_test_id_by_title(title, sectionId)
        if test_case_id == '':
            data = self.create_test_case_data(title, testType)
            print('adding new test case: ' + title)
            request = str.format('add_case/{}', sectionId)
            test_case_id = self.client.send_post(request, data)['id']
            # self.test_Case_Ids.append(test_case_id)
            return test_case_id
        else:
            # self.test_Case_Ids.append(test_case_id)
            return test_case_id

    # function to add test case result
    def add_test_case_result_for_test_run(self, testRunId, testCaseId, statusId, comment):
        """ updates a result for a test case in a given test run.
        :statusId [0=fail, 1=pass] """
        result = self.client.send_post(
            str.format('add_result_for_case/{}/{}', testRunId, testCaseId),
            {'status_id': statusId, 'comment': comment}
        )
        return result

    def add_test_case_result(self, testCaseId, statusId, comment):
        """ updates a result for a test case. No test run necessary.
        :statusId [0=fail, 1=pass] """
        result = self.client.send_post(
            str.format('add_result/{}', testCaseId),
            {'status_id': statusId, 'comment': comment}
        )
        return result

    def add_test_run_to_plan(self, testPlanId, testRunData):
        request = str.format('add_plan_entry/{}', testPlanId)
        testPlan = self.create_test_plan_data(testRunData)
        response = self.client.send_post(request, testPlan)
        print(str(response))
        return response['runs'][0]

    def create_test_run(self, testRunData, testPlanId=''):
        if testPlanId is not '':
            response = self.add_test_run_to_plan(testPlanId, testRunData)
            TestRun.test_run_id = response['id']
        else:
            request = str.format('add_run/{}', self.project_Id)
            response = self.client.send_post(request, testRunData)
            self.__current_Run_Id = response['id']
            TestRun.test_run_id = response['id']

        print('Test Run Create Response: ' + str(response))
        url = response['url']
        print('\nTEST RUN: ' + response['url'])
        return response

    def get_test_project(self):
        projects = self.client.send_get('get_projects')
        print(projects)
        self.test_project = projects
        return self.test_project

    def add_project(self, name):
        project = self.client.send_post('add_project', {'name': name})
        return project

    def get_parent_section_id(self, parentName):
        request = str.format('get_sections/{}', self.project_Id)
        sections = self.client.send_get(request)
        for section in sections:
            parentId = ''
            if section['name'] == parentName and section['depth'] == 0:
                parentId = section['id']
                return parentId
        # TODO - didn't find parent section, so create it?

    def get_section_id(self, parentSectionId, name):
        request = str.format('get_sections/{}', self.project_Id)
        sections = self.client.send_get(request)
        for section in sections:
            if section['parent_id'] == parentSectionId and section['name'] == name:
                return section['id']
        # TODO - didn't find section, so create it?

    def get_tests_in_run_by_status(self, runId, status):
        test_names = []
        request = str.format('get_tests/{}', runId)
        tests = self.client.send_get(request)
        for test in tests:
            if test['status_id'] == status:
                test_names.append(test['title'])

        return test_names

    def get_test_run_name(self, runId):
        request = str.format('get_run/{}', runId)
        test_run = self.client.send_get(request)
        return test_run['name']