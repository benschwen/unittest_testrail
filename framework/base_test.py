import unittest
import sys

# So that we can import shared modules and functions that are not selenium specific.
# you might have to do some mcguyver stuff here.  I haven't tested it.
sys.path.append("..")

from framework.attributes.test_types import TestTypeAttr


class BaseTest(unittest.TestCase):
    #
    # NEED TO SET THE PROPERTIES TO THE UNITTEST TEST CASE OBJECT SO THEY CAN BE USED DIRECTLY FROM THE TEST METHODS.
    # PROPERTIES WITH *SETTERS* NEED ONLY EXIST FOR ATTRIBUTES THAT ARE NON BUILTIN TYPES
    #

    def __get_test_method_attribute(self, attribute_name: str):
        """

        Gets an assigned test 'attribute' used from test method attributes or anything else
        typed onto the object, and returns the value

        """
        attribute = None
        try:
            attribute = getattr(
                self.__getattribute__(
                    self._testMethodName),
                attribute_name)
            return attribute
        except:
            return attribute


    @property
    def test_case_id(self):
        case_id = self.__get_test_method_attribute('test_case_id')
        if case_id == None:
            return None
        if str(case_id).__contains__('C'):
            case_id = str(case_id).replace('C', '').strip()
            return int(case_id)
        return int(case_id)

    ##### ---------> 'NON BUILTINS' PROPERTY TYPING <----------- #####
    _test_type_attribute = TestTypeAttr

    @property
    def test_type(self):
        self._test_type_attribute = self.__get_test_method_attribute('test_type')
        return self._test_type_attribute

    @test_type.setter
    def test_type(self, value):
        self._test_type_attribute = value

    _test_categories_attribute = set()

    @property
    def test_category(self):
        self._test_categories_attribute = self.__get_test_method_attribute('test_category')
        return self._test_categories_attribute

    @test_category.setter
    def test_category(self, value):
        self._test_categories_attribute = value

    ##### ---------> 'NON BUILTINS' PROPERTY TYPING <----------- #####


