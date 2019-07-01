import pytest
from tests import client, catalog, render
from flaskapp import Item
import flaskapp


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


def test_app_item_exists(client, catalog, render):
    name = "mainsheet"
    category = "sailing"
    description = "A rope used to control the main sail"
    item = Item(name=name, category=category, description=description)
    catalog.find_item.return_value = item

    client.get("sailing/mainsheet")

    assert _item_rendered_with_template(render, item, flaskapp.ITEM_TEMPLATE)


def _item_rendered_with_template(
    render_template_mock, expected_item, expected_template
):
    """
    Produce True if expected_categories were rendered by 
    render_template method using expected_template
    """
    args, kwargs = render_template_mock.call_args
    rendered_item = kwargs.get("item", None)
    template = kwargs.get("right_column_template", None)

    return (
        rendered_item
        and template
        and rendered_item == expected_item
        and template == expected_template
    )
