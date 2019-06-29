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

    assert categories_rendered_with_template(
        render_template, categories, flaskapp.CATEGORIES_TEMPLATE
    )


def categories_rendered_with_template(
    render_template_mock, expected_categories, expected_template
):
    """
    Produce True if expected_categories were rendered by 
    render_template method using expected_template
    """
    args, kwargs = render_template_mock.call_args
    rendered_categories = kwargs.get("categories", None)
    template = kwargs.get("categories_template", None)

    return (
        rendered_categories
        and template
        and rendered_categories == expected_categories
        and template == expected_template
    )


def test_retrieving_from_in_memory_catalog():
    catalog = InMemoryCatalog(["Soccer", "Baseball", "Sailing"], [])
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
