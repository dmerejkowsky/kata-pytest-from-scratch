# pytest from scratch

Goal of the kata: discover Python's way of doing things by re-implementing
a subset of pytest's functionnality using TDD and the `unittest` module - which should be
more familiar for devs coming from other languages.

## Instructions

Write a `framework.py` script that can run all the tests in `test_foo.py`:

The output should look like this:

```bash
$ python framework.py test_foo
test_answer OK
Error: test_bar_ko threw AssertionError
test_bar_ok OK
Ran 3 tests
FAILED (errors=1)
```

There are 3 things you must implement:

* Collecting all test functions
* Calling all test functions, catching errors when they occur
* Print a summary at the end

## Starting point

If you don't know where to start, you may start by this failing test:


* An empty `framework.py` file
* A first test looking like this:

```python
class RunTestCase(unittest.TestCase):
    def test_can_run_sucessful_test(self):

        # Nested functions are fine :)
        def test_equality():
            assert 1 + 1 == 2

        success = framework.run(test)

        self.assertTrue(success)
```

## Useful modules from the standard library

You probably won't need any third-party library to implement the framework.

But there are two modules from the standard library that should prove useful:

* [inspect](https://docs.python.org/3/library/inspect.html)
* [importlib](https://docs.python.org/3/library/importlib.html)

## Solution (spoiler!)

You can see one possible solution in the 
