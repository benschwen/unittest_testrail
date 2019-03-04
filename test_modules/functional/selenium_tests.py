# EXAMPLE FILE

from framework.attributes.categories import Category, UserScenario, Market
from framework.attributes.decorators import test_case_id, test_type, test_category
from framework.attributes.test_types import TestType
from framework.base_selenium_test import BaseSeleniumTest


class EcommerceSeleniumTests(BaseSeleniumTest):

    @test_case_id('C123')
    @test_type(TestType.FUNCTIONAL)
    @test_category(Category(UserScenario.ENROLLMENT))
    @test_category(Category(Market.CANADA))
    def test_run_ecommerce_enrollment(self):
    #     calls page object model to enroll customer and doesn't need to worry about anything since it's all handled in
    #     the BaseSeleniumTest
        pass