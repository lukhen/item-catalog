from flaskapp import catagories_view, render_categories_as_plain_text
from unittest.mock import Mock
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters the item-catalog web site http://localhost:5000
    He sees the list of all available categories
    """


def test_displaying_many():
    catalog = Mock()
    catalog.all_categories.return_value = ["Soccer", "Baseball", "Sailing"]
    render = Mock()

    catagories_view(catalog, render)

    render.assert_called_once_with(["Soccer", "Baseball", "Sailing"])
