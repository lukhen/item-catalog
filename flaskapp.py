from flask import Flask

app = Flask(__name__)


class InMemoryCatalog:
    def all_categories(self):
        return []


@app.route("/")
def catagories_view(catalog=InMemoryCatalog()):
    return "\n".join(catalog.all_categories())


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
