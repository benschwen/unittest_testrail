# EXAMPLE FILE

from framework.attributes.categories import Category, UserScenario, Market
from framework.attributes.decorators import test_case_id, test_type, test_category
from framework.attributes.test_types import TestType
from framework.base_test import BaseTest


class EcommerceApiTests(BaseTest):

    @test_case_id('C456')
    @test_type(TestType.INTEGRATION)
    @test_category(Category(UserScenario.ENROLLMENT))
    @test_category(Category(Market.CANADA))
    def get_ecommerce_enrollment_status(self):
    #     calls an api to get the status of some canada enrollment
        pass