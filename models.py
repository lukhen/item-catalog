import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy import ForeignKey
from flask_login import UserMixin


class CategoryException(Exception):
    ...


class ItemException(Exception):
    ...


Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String(256), unique=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(String)

    def to_dict(self):
        return dict(
            name=self.name,
            category=self.category,
            description=self.description,
            created_date=self.created_date,
        )

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
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def create_with(categories=[], items=[], db_url="sqlite:///:memory:"):
        db = SqlAlchemyCatalog(db_url)
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        db.engine = engine
        db.session = session
        db.session.add_all(categories)
        db.session.add_all(items)
        db.session.commit()
        return db

    def all_categories(self):
        return [cat[0] for cat in self.session.query(Item.category).distinct()]

    def find_item(self, item_id):
        return self.session.query(Item).filter_by(id=item_id).first()

    def category_exists(self, category):
        return category in self.all_categories()

    def category_items(self, category):
        if not self.category_exists(category):
            raise CategoryException("No such category: {}".format(category))
        else:
            return self.session.query(Item).filter_by(category=category).all()

    def add_item(self, item):
        if self.find_item(item.id) is not None:
            raise ItemException("Item [{}] already exists.".format(item))
        else:
            self.session.add(item)
            self.session.commit()

    def edit_item(self, item_id, new_name, new_category, new_description):
        item = self.find_item(item_id)
        if item:
            item.name = new_name
            item.category = new_category
            item.description = new_description
        self.session.commit()

    def delete_item(self, item):
        self.session.delete(item)
        self.session.commit()

    def recent_items(self, count):
        return list(
            self.session.query(Item)
            .order_by(Item.created_date.desc())
            .limit(count)
        )

    def all_items(self):
        return self.session.query(Item).all()
