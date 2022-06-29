import unittest

import framework
from framework import Outcome

class TestFramework(unittest.TestCase):
    def test_can_run_sucessful_test(self):

        def test_equality():
            assert 1+1 == 2


        outcome = framework.run(test_equality)
        self.assertEqual(outcome , Outcome.success)

    def test_can_run_failing_test(self):

        def failing_test():
            assert 1+1 == 3


        outcome = framework.run(failing_test)
        self.assertEqual(outcome , Outcome.failure)

