from flaskapp import InMemoryCatalog, Item


def test_item_exists():
    item = Item(name="mainsheet", category="sailing")
    catalog = InMemoryCatalog(categories=["sailing"], items=[item])
    assert catalog.find_item("sailing", "mainsheet") == item
