import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual.
    The user wants to see the description of the 'mainsheet' item
    from 'sailing' category.
    He enters the site /sailing/mainsheet.
    He can see all the information he wants: the name of the item, its
    category and description.
    """
