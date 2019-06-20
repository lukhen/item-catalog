from flask import Flask, render_template

app = Flask(__name__)


class InMemoryCatalog:
    def all_categories(self):
        return ["Soccer", "Sailing", "Football"]


def render_categories_with_template(categories):
    return render_template("categories_template.html", categories=categories)


@app.route("/")
def catagories_view(
    categories=InMemoryCatalog().all_categories(),
    render_categories=render_categories_with_template,
):
    return render_categories(categories)


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
