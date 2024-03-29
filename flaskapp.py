from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    flash,
    jsonify,
)
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    login_required,
    logout_user,
)
from models import (
    CategoryException,
    ItemException,
    Item,
    SqlAlchemyCatalog,
    User,
)
import click
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google

TWO_COLUMNS_TEMPLATE = "two_columns_template.html"
CATEGORIES_TEMPLATE = "categories_template.html"
NEW_CATEGORY_TEMPLATE = "new_category.html"
CATEGORY_ITEMS_TEMPLATE = "category_items_view.html"
ITEM_TEMPLATE = "item_template.html"
NEW_ITEM_TEMPLATE = "new_item_template.html"
DELETE_ITEM_TEMPLATE = "delete_item_template.html"
EDIT_ITEM_TEMPLATE = "edit_item_template.html"
TITLE_TEMPLATE = "title_template.html"
ITEMS_TEMPLATE = "list_of_items_template.html"

app = Flask(__name__)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
load_dotenv()

blueprint = make_google_blueprint(
    client_id="850148895071-7kitc1lgf03ooem3asrpngj8g07u0k33.apps.googleusercontent.com",
    client_secret="z4dGFMjc0pjhL2W1pWqV2oeM",
)
app.register_blueprint(blueprint, url_prefix="/login")

# SMELL: looks like a hack
catalog = SqlAlchemyCatalog(
    db_url="sqlite:///catalog.db?check_same_thread=False"
)


@click.command(name="createdb")
def create_db():
    catalog = SqlAlchemyCatalog.create_with(
        items=[], categories=[], db_url="sqlite:///catalog.db"
    )
    print("Database tables created")


app.cli.add_command(create_db)


@app.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok

    login_user(User(id=resp.json()["id"], name=resp.json()["name"]))
    return "You are @{login} on Google".format(login=resp.json()["name"])


@login_manager.user_loader
def load_user(user_id):
    if google.authorized:
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok
        user = User(id=resp.json()["id"], name=resp.json()["name"])
        if user.id == user_id:
            return user


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("categories_view"))


@app.route("/")
def categories_view():

    return render_template(
        TWO_COLUMNS_TEMPLATE,
        categories=catalog.all_categories(),
        items=catalog.recent_items(3),
        left_column_template=CATEGORIES_TEMPLATE,
        right_column_template=ITEMS_TEMPLATE,
        right_column_title="Recent Items",
        title_template=TITLE_TEMPLATE,
    )


@app.route("/<category_name>")
def category_view(category_name):
    try:
        return render_template(
            TWO_COLUMNS_TEMPLATE,
            items=catalog.category_items(category_name),
            right_column_template=CATEGORY_ITEMS_TEMPLATE,
            categories=catalog.all_categories(),
            left_column_template=CATEGORIES_TEMPLATE,
            title_template=TITLE_TEMPLATE,
            category=category_name,
        )
    except CategoryException as err:
        return abort(404)


@app.route("/catalog/<item_id>")
def item_view(item_id):
    item = catalog.find_item(item_id)
    if not item:
        abort(404)
    return render_template(
        ITEM_TEMPLATE, item=item, title_template=TITLE_TEMPLATE
    )


@app.route("/newitem", methods=["GET", "POST"])
@login_required
def new_item():
    if request.method == "GET":
        return render_template(
            NEW_ITEM_TEMPLATE,
            categories=catalog.all_categories(),
            title_template=TITLE_TEMPLATE,
        )
    else:
        catalog.add_item(
            Item(
                name=request.form["name"],
                category=request.form["category"],
                description=request.form["description"],
                user_id=current_user.id,
            )
        )
        return redirect(url_for("categories_view"))


@app.route("/catalog/<item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = catalog.find_item(item_id)

    # only users that created the item can delete it
    if item.user_id != current_user.id:
        flash(
            "You are not authorised to edit this item. {}, {}".format(
                item.user_id, current_user.id
            )
        )
        return redirect(url_for("categories_view"))
    if request.method == "GET":
        return render_template(
            EDIT_ITEM_TEMPLATE,
            item=item,
            categories=catalog.all_categories(),
            title_template=TITLE_TEMPLATE,
        )
    else:
        catalog.edit_item(
            item_id,
            request.form["name"],
            request.form["category"],
            request.form["description"],
        )
        flash("You have edited 1 item.")
        return redirect(url_for("categories_view"))


@app.route("/catalog/<item_id>/delete", methods=["GET", "POST"])
@login_required
def delete_item(item_id):
    item = catalog.find_item(item_id)

    # only users that created the item can delete it
    if item.user_id != current_user.id:
        flash(
            "You are not authorised to delete this item. {}, {}".format(
                item.user_id, current_user.id
            )
        )
        return redirect(url_for("categories_view"))
    if request.method == "GET":
        return render_template(DELETE_ITEM_TEMPLATE, item=item)
    else:
        catalog.delete_item(item)
        flash("You have deleted 1 item.")
        return redirect(url_for("categories_view"))


@app.route("/catalog/json")
def all_items():
    return jsonify([item.to_dict() for item in catalog.all_items()])


@app.route("/<category_name>/json")
def category_view_json(category_name):
    try:
        items = catalog.category_items(category_name)
        return jsonify([item.to_dict() for item in items])

    except CategoryException as err:
        return abort(404)


@app.route("/catalog/<item_id>/json")
def item_view_json(item_id):
    item = catalog.find_item(item_id)
    if not item:
        abort(404)
    return jsonify(item.to_dict())


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
