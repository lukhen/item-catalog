import flaskapp
from flaskapp import InMemoryCatalog
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
    catalog = Mock()
    categories = ["Football", "Sailing", "Baseball"]
    catalog.all_categories.return_value = categories
    client = flaskapp.app.test_client()
    flaskapp.catalog = catalog

    render_template = Mock()
    render_template.return_value = "irrelevant response output"

    temp = flaskapp.render_template
    flaskapp.render_template = render_template
    client.get("/")
    flaskapp.render_template = temp

    args, kwargs = render_template.call_args
    assert kwargs["categories"] == categories


def test_retrieving_from_in_memory_catalog():
    catalog = InMemoryCatalog(["Soccer", "Baseball", "Sailing"], [])
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
