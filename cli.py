import importlib
import sys
import framework
from framework import TestStatus
from traceback import print_tb


def main() -> None:
    name = sys.argv[1]
    module = importlib.import_module(name)
    tests = framework.collect(module)
    outcomes = []
    for test in tests:
        print(test.name)
        print("-" * len(test.name))
        outcome = framework.run(test)
        if outcome.test_status == TestStatus.success:
            print("OK")
        else:
            print("Error")
            traceback = outcome.traceback
            if traceback:
                print(traceback.type, traceback.value)
                print_tb(traceback.tb)
        print()
        outcomes.append(outcome)
    summary = framework.summarize(outcomes)
    print(f"Ran {summary.total} tests")
    if summary.errors:
        print(f"FAILED (errors={summary.errors})")
        sys.exit(1)
    else:
        print("SUCCESS")


if __name__ == "__main__":
    main()
