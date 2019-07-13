from tests import render, catalog, client
import flaskapp
from flaskapp import Item


def test_e2e():
    """
    Manual test:
    When user enters the site /catalog/123/delete the confirmation message appears.
    When the user submits the message he is shown a message confirming that the item
    has been deleted.
    """
    ...


def test_app_get(render, catalog, client):
    item = Item(id=123, name="some name", category="some category")
    catalog.find_item.side_effect = lambda item_id: item if item_id == "123" else None

    client.get("/catalog/123/delete")

    render.assert_called_once_with(flaskapp.DELETE_ITEM_TEMPLATE, item=item)


def test_app_post(render, catalog, client):
    item = Item(id=123, name="some name", category="some category")
    catalog.find_item.side_effect = lambda item_id: item if item_id == "123" else None

    client.post("/catalog/123/delete")

    catalog.delete_item.assert_called_once_with(item)
