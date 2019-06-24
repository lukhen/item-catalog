from flask import Flask, render_template, request

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

    def new_category_get(self):
        return render_template("new_category.html")

    def on_categories(self):
        return render_template(
            "categories_template.html", categories=self._catalog.all_categories()
        )


catalog = InMemoryCatalog()
controller = Controller(catalog)


@app.route("/")
def catagories_view():
    return controller.on_categories()


@app.route("/addcategory", methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        return controller.new_category_get()
    else:
        return controller.new_category_post(request.form["category_name"])


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
