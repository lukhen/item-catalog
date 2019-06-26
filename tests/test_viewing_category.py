import pytest
import flaskapp
from flask import render_template
from flaskapp import Item
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
    catalog.category_items.side_effects = (
        lambda catname: irrelevant_items if catname == "category_name" else None
    )

    client = flaskapp.app.test_client()

    flaskapp.catalog = catalog
    response = client.get("/categories/category_name")
    with flaskapp.app.app_context():
        assert (
            response.data
            == render_template(
                "category_items_view.html", items=irrelevant_items
            ).encode()
        )
