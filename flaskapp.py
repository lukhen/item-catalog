from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class Item:
    def __init__(self, name):
        ...


class InMemoryCatalog:
    def __init__(self):
        self._categories_by_name = {}

    def all_categories(self):
        return list(self._categories_by_name.keys())

    def add_category(self, category):
        self._categories_by_name[category] = category


class Controller:
    def __init__(self, catalog):
        self._catalog = catalog

    def category_requested(self, category_name):
        return render_template(
            "category_items_view.html",
            items=self._catalog.category_items(category_name),
        )


catalog = InMemoryCatalog()
controller = Controller(catalog)


@app.route("/")
def categories_view():
    return render_template(
        "categories_template.html", categories=catalog.all_categories()
    )


@app.route("/addcategory", methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        return render_template("new_category.html")
    else:
        catalog.add_category(request.form["category_name"])
        return redirect(url_for("categories_view"))


@app.route("/categories/<category_name>")
def category_view(category_name):
    return controller.category_requested(category_name)


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
