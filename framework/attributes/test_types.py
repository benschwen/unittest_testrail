class TestTypeAttr(object):
    def __init__(self,
                 name,
                 test_section_name,
                 test_section_id,
                 test_plan_id):
        self.name = name
        self.test_section_name = test_section_name
        self.test_section_id = test_section_id
        self.test_plan_id = test_plan_id


class TestType(object):
    """
    We use test types to give sorts of data to a test method about where it's test rail test case belongs.  Also,
    to establish when tests get run
    """
    # TestType EXAMPLES -->

    FUNCTIONAL = TestTypeAttr(
        name='FUNCTIONAL',
        test_section_name='Functional Tests (End to End)',
        test_section_id='142',
        test_plan_id='2772')

    WARMUP = TestTypeAttr(
        name='WARMUP',
        test_section_name="UI Node 'Warmup' Tests",
        test_section_id='557',
        test_plan_id='2773')

    INTEGRATION = TestTypeAttr(
        name='INTEGRATION',
        test_section_name='Integration Tests',
        test_section_id='558',
        test_plan_id='3232')

