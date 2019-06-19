from flaskapp import categories
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters the item-catalog web site http://localhost:5000
    He sees the list of all available categories
    """


def test_displaying_list_of_categories():
    assert categories() == ""
