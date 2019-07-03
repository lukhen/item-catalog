from flaskapp import InMemoryCatalog, Item


def test_item_not_exists():
    name = "mainsheet"
    category = "sailing"
    catalog = InMemoryCatalog()
    catalog.add_item(Item(name=name, category=category))

    assert catalog.find_item(category, name) == Item(name=name, category=category)
    assert category in catalog.all_categories()
