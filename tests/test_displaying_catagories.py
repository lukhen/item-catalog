import flaskapp
from flaskapp import categories_view, InMemoryCatalog
from unittest.mock import Mock
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters the item-catalog web site http://localhost:5000
    He sees the list of all available categories
    """


def test_app():
    controller = Mock()
    client = flaskapp.app.test_client()
    flaskapp.controller = controller
    client.get("/")

    controller.all_categories_view_requested.assert_called()


def test_retrieving_from_in_memory_catalog():
    catalog = InMemoryCatalog()
    catalog.add_category("Soccer")
    catalog.add_category("Baseball")
    catalog.add_category("Sailing")
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
