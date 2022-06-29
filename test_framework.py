import unittest

import framework
from framework import TestStatus, Test, Outcome


class CollectTestCase(unittest.TestCase):
    def test_collect_tests_in_modules(self):
        import test_foo
        from test_foo import test_bar_ok, test_bar_ko, test_answer

        tests = list(framework.collect(test_foo))

        test_functions = [t.function for t in tests]
        test_names = [t.name for t in tests]

        self.assertEqual(test_functions, [test_answer, test_bar_ko, test_bar_ok])
        self.assertEqual(test_names, ["test_answer", "test_bar_ko", "test_bar_ok"])


class RunTestCase(unittest.TestCase):
    def test_can_run_sucessful_test(self):
        def test_equality():
            assert 1 + 1 == 2

        test = Test(name="test_equality", function=test_equality)
        outcome = framework.run(test)
        self.assertEqual(outcome.test_status, TestStatus.success)
        self.assertEqual(outcome.name, "test_equality")

    def test_can_catch_exceptions(self):
        def failing_test():
            assert 1 + 1 == 3

        test = Test(name="failing_test", function=failing_test)

        outcome = framework.run(test)

        self.assertEqual(outcome.test_status, TestStatus.failure)
        self.assertIsInstance(outcome.exception, AssertionError)


class ReportTestCase(unittest.TestCase):
    def test_summary(self):
        outcomes = [
            Outcome(name="test_one", test_status=TestStatus.success),
            Outcome(
                name="test_two",
                test_status=TestStatus.failure,
                exception=KeyError("foo"),
            ),
            Outcome(name="test_three", test_status=TestStatus.success),
        ]

        summary = framework.summarize(outcomes)
        self.assertEqual(summary.total, 3)
        self.assertEqual(summary.errors, 0)
