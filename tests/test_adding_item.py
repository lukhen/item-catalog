import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters http://localhost:5000/newitem
    He can enter the name, category and description of the new item 
    and press submit button.
    Then he is redirected to http://localhost:5000/ and can see his just added item.
    """
