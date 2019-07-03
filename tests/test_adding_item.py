import flaskapp
from flaskapp import Item
import pytest
from tests import client, render, catalog


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters http://localhost:5000/newitem
    He can enter the name, category and description of the new item 
    and press submit button.
    Then he is redirected to http://localhost:5000/ and can see his just added item.
    """


def test_app_get(client, render):
    client.get("/newitem")
    assert flaskapp.NEW_ITEM_TEMPLATE in render.call_args[0]


def test_app_post(client, catalog):
    name = "::irrlevant item name::"
    category = "::irrelevant item category::"
    description = "::irrelevant item description::"

    client.post(
        "/newitem",
        data={"name": name, "category": category, "description": description},
    )

    catalog.add_item.assert_called_with(Item(name, category, description))
