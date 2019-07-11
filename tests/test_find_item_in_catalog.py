from flaskapp import InMemoryCatalog, Item, SqlAlchemyCatalog, SqlAlchemyCategory
from abc import ABC, abstractmethod


class FindItemInCatalogContract(ABC):
    @abstractmethod
    def catalog_with(self, items):
        ...

    def test_item_exists_1(self):
        item = Item(id=2, name="mainsheet", category="sailing")
        catalog = self.catalog_with(categories=["sailing"], items=[item])
        assert catalog.find_item(item.id) == item

    def test_item_exists_2(self):
        item = Item(id=5, name="ball", category="football")
        items = [Item(name="mainsheet", category="sailing"), item]
        catalog = self.catalog_with(categories=["sailing", "football"], items=items)
        assert catalog.find_item(item.id) == item


class TestFindItemInMemoryCatalog(FindItemInCatalogContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories=categories, items=items)


class TestSqlAlchemyCatalog(FindItemInCatalogContract):
    def catalog_with(self, categories, items):
        return SqlAlchemyCatalog(
            categories=[SqlAlchemyCategory(name=category) for category in categories],
            items=items,
            db_url="sqlite:///:memory:",
        )
