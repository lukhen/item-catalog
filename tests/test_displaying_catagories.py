from flaskapp import categories
from unittest.mock import Mock
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters the item-catalog web site http://localhost:5000
    He sees the list of all available categories
    """


def test_displaying_0_categories():
    catalog = Mock()
    catalog.all_categories.return_value = []
    assert categories(catalog) == ""


def test_displaying_1_category():
    catalog = Mock()
    catalog.all_categories.return_value = ["Soccer"]
    assert categories(catalog) == "Soccer"


def test_displaying_many():
    catalog = Mock()
    catalog.all_categories.return_value = ["Soccer", "Baseball", "Sailing"]
    assert categories(catalog) == "Soccer\nBaseball\nSailing"
