import sys
from typing import Type, Callable, Any
import importlib
from types import FunctionType, TracebackType
import inspect
from enum import Enum
from dataclasses import dataclass

_FIXTURES: dict[str, Callable[[], None]] = {}


def update_fixtures(name, function):
    _FIXTURES[name] = function


def get_fixture(name):
    return _FIXTURES.get(name)


@dataclass
class Test:
    name: str
    function: Callable[..., Any]


class TestStatus(Enum):
    success = "success"
    failure = "failure"


@dataclass
class Traceback:
    type: Type
    value: BaseException
    tb: TracebackType

    @classmethod
    def from_exc_info(
        cls, exc_info: tuple[Type[BaseException], BaseException, TracebackType]
    ) -> "Traceback":
        type, value, tb = exc_info
        return cls(type, value, tb)


@dataclass
class Outcome:
    name: str
    test_status: TestStatus
    traceback: Traceback | None = None


def fixture(f):
    update_fixtures(f.__name__, f)


def run(test: Test) -> Outcome:
    signature = inspect.signature(test.function)
    args: list[Any] = []
    generators: list[Any] = []
    outcome = Outcome(name=test.name, test_status=TestStatus.success, traceback=None)

    for name, parameter in signature.parameters.items():
        matching_fixture = get_fixture(name)
        if not matching_fixture:
            sys.exit(f"No such fixture: '{name}'")
        if matching_fixture:
            generator = matching_fixture()
            generators.append(generator)
            arg = next(generator)
            args.append(arg)

    try:
        test.function(*args)
    except Exception as e:
        on_test_exception(outcome)

    for generator in generators:
        try:
            next(generator)
        except StopIteration:
            pass
        except Exception as e:
            on_test_exception(outcome)

    return outcome


def on_test_exception(outcome):
    outcome.test_status = TestStatus.failure
    exc_info = sys.exc_info()
    outcome.traceback = Traceback.from_exc_info(exc_info)  # type: ignore


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
