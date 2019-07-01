import flaskapp
from flaskapp import InMemoryCatalog, render_template
from unittest.mock import Mock
import pytest


@pytest.mark.e2e
def test_e2e():
    """
    Manual test.
    When user enters the item-catalog web site http://localhost:5000
    He sees the list of all available categories
    """


@pytest.fixture
def client():
    return flaskapp.app.test_client()


@pytest.fixture
def catalog():
    temp = flaskapp.catalog
    flaskapp.catalog = Mock()
    yield flaskapp.catalog
    flaskapp.catalog = temp


@pytest.fixture
def render():
    temp = flaskapp.render_template
    flaskapp.render_template = Mock()
    yield flaskapp.render_template
    flaskapp.render_template = temp


def test_app(client, catalog, render):
    categories = ["Football", "Sailing", "Baseball"]
    catalog.all_categories.return_value = categories
    render.return_value = "irrelevant response output"

    client.get("/")

    assert categories_rendered_with_template(
        render, categories, flaskapp.CATEGORIES_TEMPLATE
    )


def categories_rendered_with_template(
    render_template_mock, expected_categories, expected_template
):
    """
    Produce True if expected_categories were rendered by 
    render_template method using expected_template
    """
    args, kwargs = render_template_mock.call_args
    rendered_categories = kwargs.get("categories", None)
    template = kwargs.get("categories_template", None)

    return (
        rendered_categories
        and template
        and rendered_categories == expected_categories
        and template == expected_template
    )


def test_rendering_one_category():
    category = "Sailing"
    with flaskapp.app.app_context():
        output = render_template(flaskapp.CATEGORIES_TEMPLATE, categories=[category])
        assert category in output


def test_rendering_many_categories():
    cat1, cat2, cat3 = "Sailing", "Football", "Baseball"
    with flaskapp.app.app_context():
        output = render_template(
            flaskapp.CATEGORIES_TEMPLATE, categories=[cat1, cat2, cat3]
        )
        assert cat1 in output and cat2 in output and cat3 in output


def test_retrieving_from_in_memory_catalog():
    catalog = InMemoryCatalog(["Soccer", "Baseball", "Sailing"], [])
    assert catalog.all_categories() == ["Soccer", "Baseball", "Sailing"]
