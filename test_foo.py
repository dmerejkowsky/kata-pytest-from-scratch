import foo


def helper_function():
    return


def test_bar_ok():
    assert foo.bar() == "bar"


def test_bar_ko():
    assert foo.bar() == "baz"


def test_answer():
    assert foo.answer() == 42
