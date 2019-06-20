from flask import Flask

app = Flask(__name__)


class InMemoryCatalog:
    def all_categories(self):
        return []


def render_categories_as_plain_text(categories):
    return "\n".join(categories)


@app.route("/")
def catagories_view(
    catalog=InMemoryCatalog(), render_categories=render_categories_as_plain_text
):
    return render_categories(catalog.all_categories())


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
