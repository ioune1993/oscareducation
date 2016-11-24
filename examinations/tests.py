from generation import needs_to_be_generated, get_variable_list, PositiveIntegerVariable


def test_detection_empty():
    assert not needs_to_be_generated("")


def test_detection_one_variable():
    assert needs_to_be_generated("{a}")


def test_get_variable_list_empty():
    assert get_variable_list("") == {}


def test_get_variable_list_one():
    assert get_variable_list("{a}") == {"a": PositiveIntegerVariable()}


def test_get_variable_list_more():
    assert get_variable_list("{a} {b}") == {"a": PositiveIntegerVariable(), "b": PositiveIntegerVariable()}


def test_get_variable_list_long():
    assert get_variable_list("{pouet}") == {"pouet": PositiveIntegerVariable()}
