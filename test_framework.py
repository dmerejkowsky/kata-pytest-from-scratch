import sys
import unittest

import framework
from framework import TestStatus, Test, Outcome, Traceback


class CollectTestCase(unittest.TestCase):
    def test_collect_tests_in_modules(self) -> None:
        import test_foo
        from test_foo import (
            test_answer,
            test_bar_ko,
            test_bar_ok,
            test_failing_to_tear_down_fixture,
            test_using_connection,
        )

        tests = list(framework.collect(test_foo))

        test_functions = [t.function for t in tests]
        test_names = [t.name for t in tests]

        self.assertEqual(
            test_functions,
            [
                test_answer,
                test_bar_ko,
                test_bar_ok,
                test_failing_to_tear_down_fixture,
                test_using_connection,
            ],
        )
        self.assertEqual(
            test_names,
            [
                "test_answer",
                "test_bar_ko",
                "test_bar_ok",
                "test_failing_to_tear_down_fixture",
                "test_using_connection",
            ],
        )


class RunTestCase(unittest.TestCase):
    def test_can_run_sucessful_test(self) -> None:
        def test_equality():
            assert 1 + 1 == 2

        test = Test(name="test_equality", function=test_equality)
        outcome = framework.run(test)
        self.assertEqual(outcome.test_status, TestStatus.success)
        self.assertEqual(outcome.name, "test_equality")

    def test_can_run_test_using_fixture(self) -> None:
        class Fixture:
            def __init__(self):
                self.state = None

        @framework.fixture
        def fixture():
            yield Fixture()

        def test_using_fixture(fixture):
            assert not fixture.state

        test = Test(name="test_using_fixture", function=test_using_fixture)
        outcome = framework.run(test)
        self.assertEqual(outcome.test_status, TestStatus.success)

    def test_can_catch_exceptions(self) -> None:
        def failing_test():
            assert 1 + 1 == 3

        test = Test(name="failing_test", function=failing_test)

        outcome = framework.run(test)

        self.assertEqual(outcome.test_status, TestStatus.failure)
        traceback = outcome.traceback
        self.assertIsNotNone(traceback)
        assert traceback
        self.assertEqual(traceback.type, AssertionError)


class ReportTestCase(unittest.TestCase):
    def test_summary(self) -> None:
        exc_info = None
        try:
            1 / 0
        except Exception as e:
            exc_info = sys.exc_info()

        assert exc_info

        outcomes = [
            Outcome(name="test_one", test_status=TestStatus.success),
            Outcome(
                name="test_two",
                test_status=TestStatus.failure,
                traceback=Traceback.from_exc_info(exc_info),  # type: ignore
            ),
            Outcome(name="test_three", test_status=TestStatus.success),
        ]

        summary = framework.summarize(outcomes)
        self.assertEqual(summary.total, 3)
        self.assertEqual(summary.errors, 1)
