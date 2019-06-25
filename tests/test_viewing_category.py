import pytest
import flaskapp
from flask import render_template
from flaskapp import Controller
from unittest.mock import Mock


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    User want te see all items of 'sailing' category.
    He enters the site /categories/sailing
    He can see all sailing items in a column.
    """


def test_app():
    controller = Mock()
    client = flaskapp.app.test_client()
    flaskapp.controller = controller
    client.get("/categories/sailing")
    controller.category_requested.assert_called_with("sailing")
