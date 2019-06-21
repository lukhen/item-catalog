from flaskapp import new_category
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


def test_rendering_newcategory_form():
    render_new_category_form = Mock()
    new_category(render_new_category_form)
    render_new_category_form.assert_called()
