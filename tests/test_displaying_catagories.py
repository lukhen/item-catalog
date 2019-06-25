import flaskapp
from flaskapp import categories_view, InMemoryCatalog
from unittest.mock import Mock
from flask import render_template
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters the item-catalog web site http://localhost:5000
    He sees the list of all available categories
    """


def test_app():
    catalog = Mock()
    categories = ["Football", "Sailing", "Baseball"]
    catalog.all_categories.return_value = categories
    client = flaskapp.app.test_client()
    flaskapp.catalog = catalog
    response = client.get("/")
    with flaskapp.app.app_context():
        assert (
            response.data
            == render_template(
                "categories_template.html", categories=categories
            ).encode()
        )


def test_retrieving_from_in_memory_catalog():
    catalog = InMemoryCatalog()
    catalog.add_category("Soccer")
    catalog.add_category("Baseball")
    catalog.add_category("Sailing")
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
