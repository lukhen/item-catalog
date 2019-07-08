from flaskapp import InMemoryCatalog, Item
from abc import ABC, abstractmethod


class FindItemInCatalogContract(ABC):
    @abstractmethod
    def catalog_with(self, items):
        ...

    def test_item_exists_1(self):
        item = Item(name="mainsheet", category="sailing")
        catalog = self.catalog_with(categories=["sailing"], items=[item])
        assert catalog.find_item("sailing", "mainsheet") == item

    def test_item_exists_2(self):
        items = [
            Item(name="mainsheet", category="sailing"),
            Item(name="ball", category="football"),
        ]
        catalog = self.catalog_with(categories=["sailing", "football"], items=items)
        assert catalog.find_item("football", "ball") == Item(
            name="ball", category="football"
        )


class TestFindItemInMemoryCatalog(FindItemInCatalogContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories=categories, items=items)
