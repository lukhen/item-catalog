from flask import Flask, render_template

app = Flask(__name__)


class InMemoryCatalog:
    def __init__(self):
        self._categories_by_name = {}

    def all_categories(self):
        return list(self._categories_by_name.keys())

    def add_category(self, category):
        self._categories_by_name[category] = category


def render_categories_with_template(categories):
    return render_template("categories_template.html", categories=categories)


def render_new_category_form():
    return render_template("new_category.html")


@app.route("/")
def catagories_view(
    categories=InMemoryCatalog().all_categories(),
    render_categories=render_categories_with_template,
):
    return render_categories(categories)


@app.route("/addcategory")
def new_category(render_new_category_form=render_new_category_form):
    return render_new_category_form()


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
