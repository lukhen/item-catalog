from flaskapp import (
    InMemoryCatalog,
    Item,
    ItemException,
    SqlAlchemyCatalog,
    SqlAlchemyCategory,
)
import pytest
from abc import ABC, abstractmethod


class AddItemToCatalogContract(ABC):
    def test_item_not_exists(self):
        name = "mainsheet"
        category = "sailing"
        catalog = self.catalog_with([], [])
        item = Item(name=name, category=category)
        catalog.add_item(item)

        assert catalog.find_item(item.id) == item
        assert category in catalog.all_categories()

    def test_item_not_exists_category_exists(self):
        name = "mainsheet"
        category = "sailing"
        catalog = self.catalog_with([category], [])

        item = Item(name=name, category=category)
        catalog.add_item(item)

        assert len(catalog.all_categories()) == 1
        assert catalog.find_item(item.id) == item

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


class TestSqlAlchemyCatalog(AddItemToCatalogContract):
    def catalog_with(self, categories, items):
        return SqlAlchemyCatalog(
            categories=[SqlAlchemyCategory(name=category) for category in categories],
            items=items,
            db_url="sqlite:///:memory:",
        )
