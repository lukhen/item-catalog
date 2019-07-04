from flaskapp import InMemoryCatalog, Item, ItemException
import pytest


def test_item_not_exists():
    name = "mainsheet"
    category = "sailing"
    catalog = InMemoryCatalog()
    catalog.add_item(Item(name=name, category=category))

    assert catalog.find_item(category, name) == Item(name=name, category=category)
    assert category in catalog.all_categories()


def test_item_not_exists_category_exists():
    name = "mainsheet"
    category = "sailing"
    catalog = InMemoryCatalog(categories=[category], items=[])

    catalog.add_item(Item(name=name, category=category))

    assert len(catalog.all_categories()) == 1
    assert catalog.find_item(category, name) == Item(name=name, category=category)


def test_item_exists():
    item = Item(name="mainsail", category="sailing")
    catalog = InMemoryCatalog(categories=["sailing"], items=[item])
    with pytest.raises(ItemException) as excinfo:
        catalog.add_item(item)
        assert "Item [{}] already exists.".format(item) in str(excinfo.value)
