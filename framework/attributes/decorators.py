# DECORATOR --->
from framework.attributes.categories import Category
from framework.attributes.test_types import TestType

def test_type(type: TestType):
    """ Used for reference to the test rail test case's test section """

    def decorator(func):
        func.test_type = type
        return func

    return decorator

# DECORATOR --->
def test_category(category: Category):
    """ Used for reference to the test rail test case's test section """

    def decorator(func) -> tuple:
        if not hasattr(func, 'test_category'):
            func.test_category = set()
        func.test_category.add(category)
        return func

    return decorator


# DECORATOR --->
def test_case_id(id):
    """ Used for reference to the test rail test case if one has already been created in test_rail"""

    def decorator(func):
        func.test_case_id = id
        return func

    return decorator


# DECORATOR --->
def test_rail_case_title(test_title):
    """
    :param test_title:  title of the test rail test case that has been set in test rail
    :return: adds an attribute to the method with this as it's decorator
    """

    def decorator(func):
        func.test_rail_case_title = test_title
        return func

    return decorator


# DECORATOR --->
def browsers_servers(browser_server_list):
    """ Sets the browsers to run the test method with
    :param browser_server_list:
    :return: adds an attribute to the function to use as a way to get the 'browsers' for the test method to run against
    """

    def decorator(func):
        func.desired_capabilities = browser_server_list
        return func

    return decorator
