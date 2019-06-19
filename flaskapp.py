from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return ""


def main():
    app.debug = True
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
