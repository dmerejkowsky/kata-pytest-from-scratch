from enum import Enum
from dataclasses import dataclass


class TestStatus(Enum):
    success = "success"
    failure = "failure"


@dataclass
class Outcome:
    test_status: TestStatus
    exception: Exception | None


def run(func) -> Outcome:
    test_status = None
    exception = None
    try:
        func()
        test_status = TestStatus.success
    except Exception as e:
        test_status = TestStatus.failure
        exception = e

    return Outcome(test_status=test_status, exception=exception)
