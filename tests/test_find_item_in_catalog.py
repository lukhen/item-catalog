from flaskapp import InMemoryCatalog, Item


def test_item_exists_1():
    item = Item(name="mainsheet", category="sailing")
    catalog = InMemoryCatalog(categories=["sailing"], items=[item])
    assert catalog.find_item("sailing", "mainsheet") == item


def test_item_exists_2():
    items = [
        Item(name="mainsheet", category="sailing"),
        Item(name="ball", category="football"),
    ]
    catalog = InMemoryCatalog(categories=["sailing", "football"], items=items)
    assert catalog.find_item("football", "ball") == Item(
        name="ball", category="football"
    )
