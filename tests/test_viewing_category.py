import pytest
import flaskapp
from flask import render_template
from flaskapp import Item, CategoryException
from unittest.mock import Mock


@pytest.mark.e2e
def test_e2e_category_exists():
    """
    Manual test.
    User wants to see all items of 'sailing' category.
    He enters the site /categories/sailing
    He can see all sailing items in a column.
    """


def test_app_category_exists():
    catalog = Mock()
    irrelevant_items = [Item("name", "category_name")]
    catalog.category_items.side_effect = (
        lambda catname: irrelevant_items if catname == "category_name" else None
    )
    # SMELL: possibly this test checks too much
    catalog.all_categories.return_value = []

    client = flaskapp.app.test_client()

    flaskapp.catalog = catalog
    response = client.get("/categories/category_name")
    with flaskapp.app.app_context():
        assert (
            render_template("category_items_view.html", items=irrelevant_items)
            in response.data.decode()
        )


def test_app_category_not_exists():
    catalog = Mock()
    error_message = "::Some irrelevant message::"
    catalog.category_items.side_effect = CategoryException(error_message)
    client = flaskapp.app.test_client()

    flaskapp.catalog = catalog
    response = client.get("/categories/not_existing_category")
    with flaskapp.app.app_context():
        assert response.status == "404 NOT FOUND"
