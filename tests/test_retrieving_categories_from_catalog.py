from flaskapp import InMemoryCatalog


def test_many_categories_in_memory_catalog():
    catalog = InMemoryCatalog(["Soccer", "Baseball", "Sailing"], [])
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
