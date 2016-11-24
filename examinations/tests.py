from generation import needs_to_be_generated, get_variable_list, render


class IntInRange():
    def __eq__(self, a):
        if a in range(1, 11):
            return True

        return False


def test_detection_empty():
    assert not needs_to_be_generated("")


def test_detection_one_variable():
    assert needs_to_be_generated("{a}")


def test_get_variable_list_empty():
    assert get_variable_list("") == {}


def test_get_variable_list_one():
    assert get_variable_list("{a}") == {"a": IntInRange()}


def test_get_variable_list_more():
    assert get_variable_list("{a} {b}") == {"a": IntInRange(), "b": IntInRange()}


def test_get_variable_list_long():
    assert get_variable_list("{pouet}") == {"pouet": IntInRange()}


def test_render_empty():
    assert render("", {}) == ""


def test_render():
    assert render("{a}", {"a": 1}) in "1"


def test_render_space():
    assert render("{ a }", {"a": 1}) in "1"


def test_render_always_the_same():
    a, a2 = render("{a} {a}", {"a": 1}).split(" ")

    assert a == a2


def test_render_always_lower_case():
    a, a2 = render("{a} {A}", {"a": 1}).split(" ")

    assert a == a2
