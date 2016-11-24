from generation import needs_to_be_generated, get_variable_list, PositiveIntegerVariable, render


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


def test_render_empty():
    assert render("") == ""


def test_render():
    assert render("{a}") in map(str, range(1, 11))


def test_render_space():
    assert render("{ a }") in map(str, range(1, 11))


def test_render_always_the_same():
    a, a2 = render("{a} {a}").split(" ")

    assert a == a2
