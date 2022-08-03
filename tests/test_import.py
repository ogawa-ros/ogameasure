import ogameasure


def test_version_is_valid():
    assert isinstance(ogameasure.__version__, str)
    assert ogameasure.__version__ not in ["", "0.0.0"]
