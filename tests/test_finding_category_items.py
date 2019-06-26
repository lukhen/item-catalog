from flaskapp import Item, InMemoryCatalog
from abc import ABC, abstractmethod


class FindingCategoryItemsContract(ABC):
    @abstractmethod
    def catalog_with(self, categories, items):
        ...

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


class TestFindingCategoryItemsInMemoryCatalog(FindingCategoryItemsContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories, items)
