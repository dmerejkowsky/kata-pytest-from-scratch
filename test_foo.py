import foo
import framework


class Connection:
    def __init__(self):
        self.state = None

    def open(self):
        print("opening ...")
        self.state = "open"

    def close(self):
        print("closing ...")
        self.state = "closed"


@framework.fixture
def connection():
    res = Connection()
    res.open()
    yield res
    res.close()


def test_using_connection(connection):
    print("asserting ...")
    assert connection.state == "open"


@framework.fixture
def error_on_close():
    yield 42
    raise Exception("Kaboom!")


def test_failing_to_tear_down_fixture(error_on_close):
    print("asserting ...")


def test_bar_ok():
    assert foo.bar() == "bar"


def test_bar_ko():
    assert foo.bar() == "baz"


def test_answer():
    assert foo.answer() == 42
