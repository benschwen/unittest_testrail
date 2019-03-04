"""

A MODULE CONTAINING ALL TEST CATEGORIES USED FOR DECORATORS TO UNITTEST.TESTCASE METHODS


To create a new Category:
Create a class that defines your category (a 'type' of category i.e. 'Applications').  Add your actual category as an
uppercase static member. Next, create an internal attribute class and give it at least 1 member called 'name'.
i.e. "I want to make a dog category to set certain attributes about my 'dog' on my test methods"

#>> example.py

## the attribute placeholder class
class _DogsAttr(object):
    def __init__(self, name, dog_name, age):
        self.name = name
        self.dog_name = dog_name
        self.age = age
        self.dog_type = 'LAB'         #:static object


## the actual category definitions
class Dogs(object):
    FAMILY_DOG = _DogsAttr('FAMILY_DOG', 'Rex', 2)
    DUMB_DOG = _DogsAttr('DUMB_DOG', 'OLD FART', 8)

usage (see: unittest_testrail.attributes.decorators.test_category)
@test_category(Category(Dogs.FAMILY_DOG))
@test_category(Category(Dogs.DUMB_DOG))
def test_print_my_family_dog(self):
    dog = self.test_category[0].category
    print('Dog Name: ' + dog.dog_name)
    print('Dog Type: ' + dog.dog_type)

#>>> Dog Name: Rex
#>>> Dog Name: LAB

you can assigned as many objects whether static or parameters as you'd like.  These objects then get 'Typed' onto
the test method (unittest.TestCase) you are running, thus giving you access to them whenever they're loaded into
a unittest.TestSuite, or, access to certain contextual objects inside of the test method itself.

"""


class Category(object):
    def __init__(self, object):
        self.category = object

# SOME EXAMPLE CATEGORIES ->
class _ApplicationAttr(object):
    def __init__(self, name):
        self.name = name


class Applications(object):
    ECOMMERCE = _ApplicationAttr('ECOMMERCE')
    HR = _ApplicationAttr('HR')
    WAREHOUSE = _ApplicationAttr('WAREHOUSE')

class _SpecialDeliveryAttr(object):
    def __init__(self, name):
        self.name = name


class SpecialDelivery(object):
    HAWAII = _SpecialDeliveryAttr('HAWAII')
    ALASKA = _SpecialDeliveryAttr('ALASKA')
    POBOX = _SpecialDeliveryAttr('POBOX')


class _UserScenario(object):
    def __init__(self, name):
        self.name = name


class UserScenario(object):
    ENROLLMENT = _UserScenario('ENROLLMENT')

class _MarketAttr(object):
    def __init__(self, name, currency=''):
        self.name = name
        self.currency = currency

class Market(object):
    CANADA = _MarketAttr('CANADA', 'USD')