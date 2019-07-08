from flaskapp import InMemoryCatalog, SqlAlchemyCatalog, SqlAlchemyCategory
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


class TestSqlAlchemyCatalog(RetrievingCategoriesFromCatalogContract):
    def catalog_with(self, categories, items):
        return SqlAlchemyCatalog(
            categories=[SqlAlchemyCategory(name=category) for category in categories],
            items=items,
            db_url="sqlite:///:memory:",
        )
