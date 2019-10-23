from main import get_joke


def test_get_joke():
    joke = get_joke()
    assert isinstance(joke, str)
    assert len(joke) > 0
