from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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

    def new_category_form_requested(self):
        return render_template("new_category.html")

    def all_categories_view_requested(self):
        return render_template(
            "categories_template.html", categories=self._catalog.all_categories()
        )

    def new_category_posted(self, category):
        self._catalog.add_category(category)


catalog = InMemoryCatalog()
controller = Controller(catalog)


@app.route("/")
def categories_view():
    return controller.all_categories_view_requested()


@app.route("/addcategory", methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        return controller.new_category_form_requested()
    else:
        controller.new_category_posted(request.form["category_name"])
        return redirect(url_for("categories_view"))


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
