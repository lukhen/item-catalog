from flaskapp import InMemoryCatalog
from abc import ABC, abstractmethod


class RetrievingCategoriesFromCatalogContract(ABC):
    def test_many(self):
        catalog = self.catalog_with(
            categories=["Soccer", "Baseball", "Sailing"], items=[]
        )
        assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]

    @abstractmethod
    def catalog_with(self, categories, items):
        ...


class TestInMemoryCatalog(RetrievingCategoriesFromCatalogContract):
    def catalog_with(self, categories, items):
        return InMemoryCatalog(categories=categories, items=items)
