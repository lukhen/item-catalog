import pytest
import sys
import requests


@pytest.mark.e2e
def test_e2e():
    """
    This is the first teeny-tiny feature of the item-catalog app.
    I call this test the 'walking skeleton', after Nat Pryce in his book.
    It serves the purpose of setting up the skeleton of the application.
    It has to be automated and totally end to end.
    Totally means really 'totally', along with automatically installing the app
    and running it.

    User story:
    A new-comming user enters the item-catalog web site http://localhost:5000.
    The page loads without any errors.
    """

    install_app_from_github()
    run_app()

    resp = requests.get("http://localhost:5000")

    assert resp.status_code == 200


def install_app_from_github():
    ...


def run_app():
    ...
