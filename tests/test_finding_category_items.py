from flaskapp import Item, InMemoryCatalog


class TestInMemoryCatalog:
    def test_category_exists_and_only_one_category(self):
        categories = ["Sailing", "Football"]
        sailing_items = [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
        ]
        catalog = InMemoryCatalog(categories, sailing_items)
        category_name = "Sailing"
        assert catalog.category_items(category_name) == sailing_items

    def test_category_exists_multiple_categories(self):
        categories = ["Sailing", "Football"]
        items = [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
            Item("ball", "Football"),
            Item("gloves", "Football"),
        ]
        catalog = InMemoryCatalog(categories, items)
        assert catalog.category_items("Sailing") == [
            Item("mainsheet", "Sailing"),
            Item("mainsail", "Sailing"),
            Item("rudder", "Sailing"),
        ]
