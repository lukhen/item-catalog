from flaskapp import (
    Item,
    InMemoryCatalog,
    CategoryException,
    SqlAlchemyCatalog,
    SqlAlchemyCategory,
)
from abc import ABC, abstractmethod
import pytest


class FindingCategoryItemsInCatalogContract(ABC):
    @abstractmethod
    def catalog_with(self, categories, items):
        ...

    def test_category_exists_zero_items_in_category(self):
        categories = ["Sailing", "Football"]
        sailing_items = [Item(name="mainsail", category="Sailing")]
        catalog = self.catalog_with(categories, sailing_items)

        assert catalog.category_items("Football") == []

    def test_category_exists_and_only_one_category(self):
        categories = ["Sailing", "Football"]
        sailing_items = [
            Item(name="mainsheet", category="Sailing"),
            Item(name="mainsail", category="Sailing"),
            Item(name="rudder", category="Sailing"),
        ]
        catalog = self.catalog_with(categories, sailing_items)
        category_name = "Sailing"
        assert catalog.category_items(category_name) == sailing_items

    def test_category_exists_multiple_categories(self):
        categories = ["Sailing", "Football"]
        items = [
            Item(name="mainsheet", category="Sailing"),
            Item(name="mainsail", category="Sailing"),
            Item(name="rudder", category="Sailing"),
            Item(name="ball", category="Football"),
            Item(name="gloves", category="Football"),
        ]
        catalog = self.catalog_with(categories, items)
        assert catalog.category_items("Sailing") == [
            Item(name="mainsheet", category="Sailing"),
            Item(name="mainsail", category="Sailing"),
            Item(name="rudder", category="Sailing"),
        ]

    def test_category_exists_and_the_same_names_in_different_categories(self):
        categories = ["Sailing", "Football"]
        items = [
            Item(name="mainsheet", category="Sailing"),
            Item(name="mainsail", category="Sailing"),
            Item(name="rudder", category="Sailing"),
            Item(name="ball", category="Football"),
            Item(name="gloves", category="Football"),
            Item(name="gloves", category="Sailing"),
        ]
        catalog = self.catalog_with(categories, items)
        assert catalog.category_items("Sailing") == [
            Item(name="mainsheet", category="Sailing"),
            Item(name="mainsail", category="Sailing"),
            Item(name="rudder", category="Sailing"),
            Item(name="gloves", category="Sailing"),
        ]

    def test_category_not_exists(self):
        with pytest.raises(CategoryException) as excinfo:
            catalog = self.catalog_with(["Football"], [])
            catalog.category_items("Sailing")
        assert "No such category: {}".format("Sailing") in str(excinfo.value)


class TestFindingCategoryItemsInMemoryCatalog(FindingCategoryItemsInCatalogContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories, items)


class TestSqlAlchemyCatalog(FindingCategoryItemsInCatalogContract):
    def catalog_with(self, categories, items):
        return SqlAlchemyCatalog(
            categories=[SqlAlchemyCategory(name=category) for category in categories],
            items=items,
            db_url="sqlite:///:memory:",
        )
