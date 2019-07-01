import pytest
import flaskapp
from unittest.mock import Mock


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
