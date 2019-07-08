from flaskapp import Item


def test_equal():
    i1 = Item(name="mainsail", category="sailing")
    i2 = Item(name="mainsail", category="sailing")
    assert i1 == i2
