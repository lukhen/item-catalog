from models import Item
from flask import render_template
import flaskapp


def test_one_item():
    item = Item(
        category="sailing",
        name="mainsheet",
        description="A rope to manipulate the mainsail.",
    )
    with flaskapp.app.app_context():
        output = render_template(flaskapp.ITEM_TEMPLATE, item=item)
        assert item.name in output and item.description in output
