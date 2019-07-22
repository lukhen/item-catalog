from flask_login import current_user, login_user
import flaskapp
from models import User


def test_not_logged_in():
    user = current_user
    assert user == None


def test_logged_in():
    with flaskapp.app.test_request_context():
        login_user(User(email="email@somedomain"))
        assert current_user.email == "email@somedomain"
