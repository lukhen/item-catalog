from flask import Flask, render_template, request, redirect, url_for, abort

MAIN_LAYOUT_TEMPLATE = "layout.html"
CATEGORIES_TEMPLATE = "categories_template.html"
NEW_CATEGORY_TEMPLATE = "new_category.html"
ITEMS_TEMPLATE = "category_items_view.html"
ITEM_TEMPLATE = "item_template.html"


app = Flask(__name__)


class CategoryException(Exception):
    ...


class Item:
    def __init__(self, name, category, description=""):
        self.name = name
        self.category = category
        self.description = description

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name and self.category == other.category

    def __repr__(self):
        return "<Item: name={}, category={}, description={}>".format(
            self.name, self.category, self.description
        )


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

    def find_item(self, category, name):
        for item in self._items:
            if item.name == name and item.category == category:
                return item
        return None


catalog = InMemoryCatalog([], [])


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


@app.route("/<category_name>/<item_name>")
def item_view(category_name, item_name):
    return render_template(
        MAIN_LAYOUT_TEMPLATE,
        item=catalog.find_item(category_name, item_name),
        right_column_template=ITEM_TEMPLATE,
        left_column_template=CATEGORIES_TEMPLATE,
    )


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
