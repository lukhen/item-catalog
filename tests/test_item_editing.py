import flaskapp
from flaskapp import Item
import pytest
from tests import client, render, catalog


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters http://localhost:5000/catalog/123/edit
    He can change the name, category and description of the item with id 123 
    and press submit button.
    Then he is redirected to http://localhost:5000/catalog/123 and can see his 
    just edited  item.
    """


def test_item_rendered_with_new_item_template(client, render, catalog):
    item = Item(id=123, name="irrelevant name", category="irrelevant category")
    catalog.find_item.side_effect = lambda item_id: item if item_id == "123" else None

    client.get("/catalog/123/edit")

    assert (
        flaskapp.NEW_ITEM_TEMPLATE in render.call_args[0]
        and render.call_args[1].get("item", None) == item
    )


def test_app_post(client, catalog):
    new_name = "::irrlevant item name::"
    new_category = "::irrelevant item category::"
    new_description = "::irrelevant item description::"

    client.post(
        "/catalog/123/edit",
        data={
            "name": new_name,
            "category": new_category,
            "description": new_description,
        },
    )

    catalog.edit_item.assert_called_with("123", new_name, new_category, new_description)
