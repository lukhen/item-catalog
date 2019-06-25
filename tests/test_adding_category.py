import flaskapp
from flask import render_template
from flaskapp import Controller
from unittest.mock import Mock
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters http://localhost:5000/addcategory
    He can enter the name of a new category and press submit button.
    Then he is redirected to http://localhost:5000/categories and can see his just added category.
    """


def test_app_get():
    client = flaskapp.app.test_client()
    response = client.get("/addcategory")
    with flaskapp.app.app_context():
        assert (
            response.data
            == render_template(
                "new_category.html", categories=["Football", "Sailing"]
            ).encode()
        )


def test_app_post():
    client = flaskapp.app.test_client()
    catalog = Mock()
    flaskapp.catalog = catalog
    new_category = "Programming"
    client.post("/addcategory", data={"category_name": new_category})
    catalog.add_category.assert_called_with(new_category)
