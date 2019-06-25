import pytest
import flaskapp
from flask import render_template
from flaskapp import Item
from unittest.mock import Mock


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    User wants to see all items of 'sailing' category.
    He enters the site /categories/sailing
    He can see all sailing items in a column.
    """


def test_app():
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
