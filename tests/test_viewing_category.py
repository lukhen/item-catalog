import pytest
import flaskapp
from flask import render_template
from flaskapp import Item, InMemoryCatalog
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
    category_name = "sailing"
    sailing_items = [Item("mainsheet"), Item("mainsail"), Item("rudder")]
    catalog.category_items.side_effects = (
        lambda catname: sailing_items if catname == category_name else None
    )

    client = flaskapp.app.test_client()

    flaskapp.catalog = catalog
    response = client.get("/categories/sailing")
    with flaskapp.app.app_context():
        assert (
            response.data
            == render_template("category_items_view.html", items=sailing_items).encode()
        )


def test_in_memory_catalog_category_exists_and_only_one_category():
    categories = ["Sailing", "Football"]
    sailing_items = [Item("mainsheet"), Item("mainsail"), Item("rudder")]
    catalog = InMemoryCatalog(categories, sailing_items)
    category_name = "Sailing"
    assert catalog.category_items(category_name) == sailing_items
