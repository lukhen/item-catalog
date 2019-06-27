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
            render_template("categories_template.html", categories=categories)
            in response.data.decode()
        )


def test_retrieving_from_in_memory_catalog():
    catalog = InMemoryCatalog(["Soccer", "Baseball", "Sailing"], [])
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
