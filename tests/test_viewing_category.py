import pytest
import flaskapp
from flask import render_template
from flaskapp import Item, CategoryException
from unittest.mock import Mock
from tests import client, catalog, render


@pytest.mark.e2e
def test_e2e_category_exists():
    """
    Manual test.
    User wants to see all items of 'sailing' category.
    He enters the site /sailing
    He can see all sailing items in a column.
    """


def test_app_category_exists(client, catalog, render):
    irrelevant_items = [Item("name", "category_name")]
    catalog.category_items.side_effect = (
        lambda catname: irrelevant_items if catname == "category_name" else None
    )

    client.get("/category_name")

    assert _items_rendered_with_template(
        render, irrelevant_items, flaskapp.ITEMS_TEMPLATE
    )


def test_app_category_not_exists(client):
    catalog = Mock()
    error_message = "::Some irrelevant message::"
    catalog.category_items.side_effect = CategoryException(error_message)

    flaskapp.catalog = catalog
    response = client.get("/not_existing_category")
    with flaskapp.app.app_context():
        assert response.status == "404 NOT FOUND"


def _items_rendered_with_template(
    render_template_mock, expected_items, expected_template
):
    """
    Produce True if expected_items were rendered by 
    render_template method using expected_template
    """
    args, kwargs = render_template_mock.call_args
    rendered_items = kwargs.get("items", None)
    template = kwargs.get("items_template", None)

    return (
        rendered_items
        and template
        and rendered_items == expected_items
        and template == expected_template
    )
