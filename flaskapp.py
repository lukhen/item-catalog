from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

MAIN_LAYOUT_TEMPLATE = "layout.html"
CATEGORIES_TEMPLATE = "categories_template.html"
NEW_CATEGORY_TEMPLATE = "new_category.html"
ITEMS_TEMPLATE = "category_items_view.html"
ITEM_TEMPLATE = "item_template.html"
NEW_ITEM_TEMPLATE = "new_item_template.html"

app = Flask(__name__)


class CategoryException(Exception):
    ...


class ItemException(Exception):
    ...


class InMemoryCatalog:
    def __init__(self, categories=[], items=[]):
        self._categories = categories
        self._items = items

    def all_categories(self):
        return self._categories

    def add_category(self, category):
        if not self.category_exists(category):
            self._categories.append(category)

    def category_exists(self, category):
        return category in self._categories

    def category_items(self, category):
        if category not in self._categories:
            raise CategoryException("No such category: {}".format(category))
        return [item for item in self._items if item.category == category]

    def find_item(self, item_id):
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def add_item(self, item):
        self.add_category(item.category)
        if self.item_exists(item):
            raise ItemException("Item [{}] already exists.".format(item))
        self._items.append(item)

    def item_exists(self, item):
        return item in self._items


Base = declarative_base()


class SqlAlchemyCategory(Base):
    __tablename__ = "categories"

    name = Column(String, primary_key=True)

    def __repr__(self):
        return "<Category: name={}>".format(self.name)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name and self.category == other.category

    def __repr__(self):
        return "<Item: name={}, category={}, description={}>".format(
            self.name, self.category, self.description
        )


class SqlAlchemyCatalog:
    def __init__(self, categories=[], items=[], db_url="sqlite:///:memory:"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.add_all(categories)
        self.session.add_all(items)
        self.session.commit()

    def all_categories(self):
        return [cat.name for cat in self.session.query(SqlAlchemyCategory).all()]

    def find_item(self, item_id):
        return self.session.query(Item).filter_by(id=item_id).first()

    def category_exists(self, category):
        return self.session.query(SqlAlchemyCategory).filter_by(name=category).first()

    def category_items(self, category):
        if not self.category_exists(category):
            raise CategoryException("No such category: {}".format(category))
        else:
            return self.session.query(Item).filter_by(category=category).all()

    def add_category(self, category):
        if not self.category_exists(category):
            self.session.add(SqlAlchemyCategory(name=category))
            self.session.commit()

    def add_item(self, item):
        self.add_category(item.category)
        if self.find_item(item.id) is not None:
            raise ItemException("Item [{}] already exists.".format(item))
        else:
            self.session.add(item)
            self.session.commit()


catalog = InMemoryCatalog([], [])
catalog = SqlAlchemyCatalog(categories=[], items=[], db_url="sqlite:///catalog.db")


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


@app.route("/catalog/<item_id>")
def item_view(item_id):
    item = catalog.find_item(item_id)
    if not item:
        abort(404)
    return render_template(
        MAIN_LAYOUT_TEMPLATE,
        item=item,
        right_column_template=ITEM_TEMPLATE,
        left_column_template=CATEGORIES_TEMPLATE,
    )


@app.route("/newitem", methods=["GET", "POST"])
def new_item():
    if request.method == "GET":
        return render_template(NEW_ITEM_TEMPLATE)
    else:
        catalog.add_item(
            Item(
                name=request.form["name"],
                category=request.form["category"],
                description=request.form["description"],
            )
        )
        return redirect(url_for("categories_view"))


@app.route("/catalog/<item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    item = catalog.find_item(item_id)
    if request.method == "GET":
        return render_template(NEW_ITEM_TEMPLATE, item=item)
    else:
        catalog.edit_item(
            item_id,
            request.form["name"],
            request.form["category"],
            request.form["description"],
        )
        return ""


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
