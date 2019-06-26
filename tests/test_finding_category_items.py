from flaskapp import Item, InMemoryCatalog, CategoryException
from abc import ABC, abstractmethod
import pytest


class FindingCategoryItemsContract(ABC):
    @abstractmethod
    def catalog_with(self, categories, items):
        ...

    def test_category_exists_zero_items_in_category(self):
        categories = ["Sailing", "Football"]
        sailing_items = [Item("mainsail", "Sailing")]
        catalog = self.catalog_with(categories, sailing_items)

        assert catalog.category_items("Football") == []

    def test_category_exists_and_only_one_category(self):
        categories = ["Sailing", "Football"]
        sailing_items = [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
        ]
        catalog = self.catalog_with(categories, sailing_items)
        category_name = "Sailing"
        assert catalog.category_items(category_name) == sailing_items

    def test_category_exists_multiple_categories(self):
        categories = ["Sailing", "Football"]
        items = [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
            Item("ball", "Football"),
            Item("gloves", "Football"),
        ]
        catalog = self.catalog_with(categories, items)
        assert catalog.category_items("Sailing") == [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
        ]

    def test_category_exists_and_the_same_names_in_different_categories(self):
        categories = ["Sailing", "Football"]
        items = [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
            Item("ball", "Football"),
            Item("gloves", "Football"),
            Item("gloves", "Sailing"),
        ]
        catalog = self.catalog_with(categories, items)
        assert catalog.category_items("Sailing") == [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
            Item("gloves", "Sailing"),
        ]

    def test_category_not_exists(self):
        with pytest.raises(CategoryException) as excinfo:
            catalog = self.catalog_with(["Football"], [])
            catalog.category_items("Sailing")
        assert "No such category: {}".format("Sailing") in str(excinfo.value)


class TestFindingCategoryItemsInMemoryCatalog(FindingCategoryItemsContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories, items)
