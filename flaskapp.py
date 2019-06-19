from flask import Flask

app = Flask(__name__)


class InMemoryCatalog:
    def all_categories(self):
        return []


@app.route("/")
def categories(catalog=InMemoryCatalog()):
    all_cats = catalog.all_categories()
    if all_cats:
        return all_cats[0]
    else:
        return ""


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
