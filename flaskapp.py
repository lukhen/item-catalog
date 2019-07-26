from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, current_user, login_user, login_required
from models import (
    CategoryException,
    ItemException,
    Item,
    SqlAlchemyCatalog,
    InMemoryCatalog,
    User,
)
import click
from dotenv import load_dotenv

MAIN_LAYOUT_TEMPLATE = "layout.html"
CATEGORIES_TEMPLATE = "categories_template.html"
NEW_CATEGORY_TEMPLATE = "new_category.html"
ITEMS_TEMPLATE = "category_items_view.html"
ITEM_TEMPLATE = "item_template.html"
NEW_ITEM_TEMPLATE = "new_item_template.html"
DELETE_ITEM_TEMPLATE = "delete_item_template.html"


app = Flask(__name__)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
load_dotenv()

catalog = SqlAlchemyCatalog(db_url="sqlite:///catalog.db")


@click.command(name="createdb")
def create_db():
    catalog = SqlAlchemyCatalog.create_with(
        items=[], categories=[], db_url="sqlite:///catalog.db"
    )
    print("Database tables created")


app.cli.add_command(create_db)


@app.route("/login")
def login():
    return "login"


@login_manager.user_loader
def load_user(user_id):
    return catalog.find_user(user_id)


@app.route("/")
def categories_view():
    return render_template(
        MAIN_LAYOUT_TEMPLATE,
        categories=catalog.all_categories(),
        items=[],
        left_column_template=CATEGORIES_TEMPLATE,
        right_column_template=ITEMS_TEMPLATE,
    )


@app.route("/addcategory", methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        return render_template(NEW_CATEGORY_TEMPLATE)
    else:
        catalog.add_category(request.form["category_name"])
        return redirect(url_for("categories_view"))


@app.route("/<category_name>")
def category_view(category_name):
    try:
        items = catalog.category_items(category_name)
        return render_template(
            MAIN_LAYOUT_TEMPLATE,
            items=items,
            right_column_template=ITEMS_TEMPLATE,
            categories=catalog.all_categories(),
            left_column_template=CATEGORIES_TEMPLATE,
        )
    except CategoryException as err:
        return abort(404)


@app.route("/catalog/<item_id>")
def item_view(item_id):
    item = catalog.find_item(item_id)
    if not item:
        abort(404)
    return render_template(
        MAIN_LAYOUT_TEMPLATE,
        item=item,
        right_column_template=ITEM_TEMPLATE,
        left_column_template=CATEGORIES_TEMPLATE,
    )


@app.route("/newitem", methods=["GET", "POST"])
@login_required
def new_item():
    if request.method == "GET":
        return render_template(NEW_ITEM_TEMPLATE)
    else:
        catalog.add_item(
            Item(
                name=request.form["name"],
                category=request.form["category"],
                description=request.form["description"],
            )
        )
        return redirect(url_for("categories_view"))


@app.route("/catalog/<item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    item = catalog.find_item(item_id)
    if request.method == "GET":
        return render_template(NEW_ITEM_TEMPLATE, item=item)
    else:
        catalog.edit_item(
            item_id,
            request.form["name"],
            request.form["category"],
            request.form["description"],
        )
        return ""


@app.route("/catalog/<item_id>/delete", methods=["GET", "POST"])
def delete_item(item_id):
    item = catalog.find_item(item_id)
    if request.method == "GET":
        return render_template(DELETE_ITEM_TEMPLATE, item=item)
    else:
        catalog.delete_item(item)


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
