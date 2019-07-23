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


@pytest.fixture
def redirect_mock():
    temp = flaskapp.redirect
    flaskapp.redirect = Mock()
    yield flaskapp.redirect
    flaskapp.redirect = temp


@pytest.fixture
def current_user_mock():
    temp = flaskapp.current_user
    flaskapp.current_user = Mock()
    yield flaskapp.current_user
    flaskapp.current_user = temp
