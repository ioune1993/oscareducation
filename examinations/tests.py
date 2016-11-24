from generation import needs_to_be_generated


def test_detection_empty():
    assert not needs_to_be_generated("")


def test_detection_one_variable():
    assert needs_to_be_generated("{a}")
