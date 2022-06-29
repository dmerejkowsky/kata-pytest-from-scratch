import sys
import importlib
import types
import inspect
from enum import Enum
from dataclasses import dataclass


@dataclass
class Test:
    name: str
    function: types.FunctionType


class TestStatus(Enum):
    success = "success"
    failure = "failure"


@dataclass
class Outcome:
    name: str
    test_status: TestStatus
    exception: Exception | None = None


def run(test: Test) -> Outcome:
    test_status = None
    exception = None
    try:
        test.function()
        test_status = TestStatus.success
    except Exception as e:
        test_status = TestStatus.failure
        exception = e

    return Outcome(name=test.name, test_status=test_status, exception=exception)


def collect(module):
    for name, value in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("test_"):
            yield Test(name=name, function=value)


@dataclass
class Summary:
    total: int
    errors: int


def summarize(outcomes):
    total = len(outcomes)
    errors = len([o for o in outcomes if o.test_status != TestStatus.success])
    return Summary(total=total, errors=errors)


def main():
    name = sys.argv[1]
    module = importlib.import_module(name)
    tests = collect(module)
    outcomes = []
    for test in tests:
        outcome = run(test)
        if outcome.test_status == TestStatus.success:
            print(test.name, "OK")
        else:
            print("Error:", test.name, "threw", outcome.exception.__class__.__name__)
        outcomes.append(outcome)
    summary = summarize(outcomes)
    print(f"Ran {summary.total} tests")
    if summary.errors:
        print(f"FAILED (errors={summary.errors})")
        sys.exit(1)
    else:
        print("SUCCESS")


if __name__ == "__main__":
    main()
