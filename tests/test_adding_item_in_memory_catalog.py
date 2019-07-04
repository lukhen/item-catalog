from flaskapp import InMemoryCatalog, Item, ItemException
import pytest
from abc import ABC, abstractmethod


class AddItemToCatalogContract(ABC):
    def test_item_not_exists(self):
        name = "mainsheet"
        category = "sailing"
        catalog = self.catalog_with([], [])
        catalog.add_item(Item(name=name, category=category))

        assert catalog.find_item(category, name) == Item(name=name, category=category)
        assert category in catalog.all_categories()

    def test_item_not_exists_category_exists(self):
        name = "mainsheet"
        category = "sailing"
        catalog = self.catalog_with([category], [])

        catalog.add_item(Item(name=name, category=category))

        assert len(catalog.all_categories()) == 1
        assert catalog.find_item(category, name) == Item(name=name, category=category)

    def test_item_exists(self):
        item = Item(name="mainsail", category="sailing")
        catalog = self.catalog_with(["sailing"], [item])
        with pytest.raises(ItemException) as excinfo:
            catalog.add_item(item)
            assert "Item [{}] already exists.".format(item) in str(excinfo.value)

    @abstractmethod
    def catalog_with(categories, items):
        ...


class TestAddItemToInMemoryCatalog(AddItemToCatalogContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories=categories, items=items)
