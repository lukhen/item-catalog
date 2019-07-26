from flask import url_for
import flaskapp
from models import Item
import pytest
from tests import client, render, catalog, redirect_mock, current_user_mock


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters http://localhost:5000/newitem
    He can enter the name, category and description of the new item 
    and press submit button.
    Then he is redirected to http://localhost:5000/ and can see his just added item.
    """


def test_app_get_request_while_user_logged_in(client, render, current_user_mock):
    with flaskapp.app.test_request_context():
        flaskapp.app.config["LOGIN_DISABLED"] = True
        flaskapp.login_manager.init_app(flaskapp.app)
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

    catalog.add_item.assert_called_with(
        Item(name=name, category=category, description=description)
    )
