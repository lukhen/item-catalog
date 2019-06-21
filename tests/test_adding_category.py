import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters http://localhost:5000/addcategory
    He can enter the name of a new category and press submit button.
    Then he is redirected to http://localhost:5000/categories and can see his just added category.
    """
