from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class CategoryException(Exception):
    ...


class Item:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __eq__(self, other):
        return self.name == other.name and self.category == other.category

    def __repr__(self):
        return "<Item: name={}, category={}>".format(self.name, self.category)


class InMemoryCatalog:
    def __init__(self, categories=[], items=[]):
        self._categories = categories
        self._items = items

    def all_categories(self):
        return self._categories

    def add_category(self, category):
        self._categories.append(category)

    def category_items(self, category):
        if category not in self._categories:
            raise CategoryException("No such category: {}".format(category))
        return [item for item in self._items if item.category == category]


catalog = InMemoryCatalog([], [])


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
    return render_template(
        "category_items_view.html", items=catalog.category_items(category_name)
    )


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
