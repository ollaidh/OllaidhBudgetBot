import os
import time

from google.cloud.firestore import Client
from google.cloud import firestore
from typing import Optional
from date_utils import *
from db_adapters.adapter import PurchaseInfo


# TODO: transactions!
class FirestoreAdapter:
    def __init__(self, sleep_wait_ms: int = 0):
        """
        Initializes a FirestoreAdapter instance.

        :param sleep_wait_ms: The amount of time, in milliseconds, to wait between operations.
                             Default is 0, indicating no sleep/wait time.
                             (only for testing purposes)

        :raises ValueError: If the sleep_wait_ms parameter is not an integer.
        """
        project_id = os.getenv("BUDBOT_PROJECT_ID")
        self.db = Client(project=project_id)
        self.sleep_wait_ms = sleep_wait_ms  # used for race condition tests, = 0 in production
        self.purchase_categories = self.get_purchase_categories()

    def add_purchase(self, purchase: PurchaseInfo) -> bool:
        transaction = self.db.transaction()

        @firestore.transactional
        def add(trans) -> bool:
            try:
                month_database = self.db.collection("months").document(get_month_today())
                data = month_database.get(transaction=trans).to_dict()
                if data:
                    last_id = int(data["last_id"])
                    last_id += 1
                else:
                    trans.set(month_database, {"last_id": "0"})
                    last_id = 0
                if self.sleep_wait_ms > 0:
                    time.sleep(self.sleep_wait_ms / 1000)  # artificially turns on >0 in tests to test race condition
                trans.set(month_database, {"last_id": str(last_id)})

                curr_purchase = month_database.collection("items").document(str(last_id))
                trans.set(
                    curr_purchase,
                    {
                        "purchase": purchase.name,
                        "price": purchase.price,
                        "category": purchase.category,
                        "date": get_date_today(),
                    },
                )
                return True
            except Exception as err:
                print(err)
                return False

        return add(transaction)

        # @firestore.transactional

    def delete_purchase(self) -> bool:
        try:
            last_id = self.db.collection("months").document(get_month_today()).get().to_dict()["last_id"]
            if last_id:
                self.db.collection("months").document(get_month_today()).collection("items").document(
                    str(last_id)
                ).delete()
                self.db.collection("months").document(get_month_today()).update({"last_id": str(int(last_id) - 1)})
            return True
        except:
            return False

    def calculate_spent(self, start_date: str, end_date: str, category: str) -> Optional[dict]:
        try:
            months = months_spent(start_date, end_date)
            spent: dict = {}

            def add_to_spent(cat, price):
                spent[cat] = spent.get(cat, 0) + price

            for month in months:
                items = self.db.collection("months").document(month).collection("items").get()
                if not items:
                    continue
                for item in items:
                    if category not in [item.to_dict()["category"], "$all", "$each"]:
                        continue
                    if category == "$all":
                        add_to_spent(category, item.to_dict()["price"])
                    elif category == "$each":
                        add_to_spent(item.to_dict()["category"], item.to_dict()["price"])
                    else:
                        add_to_spent(item.to_dict()["category"].upper(), item.to_dict()["price"])
                        add_to_spent(item.to_dict()["purchase"], item.to_dict()["price"])
            if category == "$each" and spent:
                spent_total = 0
                for key in spent:
                    spent_total += spent[key]
                spent["TOTAL"] = spent_total
            result = {k: v for k, v in sorted(spent.items(), key=lambda x: -x[1])}
            return result
        except:
            return None

    def set_month_limit(self, limit) -> bool:
        """
        Set how much money you wish to spend during current month - for burndown tracking.
        If month spend limit already set, new value will overwrite it
        """

        transaction = self.db.transaction()

        @firestore.transactional
        def set_limit(trans, limit) -> bool:
            try:
                settings_database = self.db.collection("settings").document("month_spend_limit")
                trans.set(settings_database, {"month_spend_limit": limit})
                return True
            except Exception as err:
                print(err)
                return False

        return set_limit(transaction, limit)

    def get_month_limit(self) -> str:
        """
        Get spend limit for certain month, if not month passed then for current month
        """

        transaction = self.db.transaction()

        @firestore.transactional
        def get_limit(trans) -> bool:
            try:
                settings_database = self.db.collection("settings").document("month_spend_limit")
                limit = settings_database.get().to_dict().get("month_spend_limit")
                return limit
            except Exception as err:
                print(err)
                return False

        return get_limit(transaction)
    
    # def set_purchase_category(self, purchase, category) -> bool:
    #     transaction = self.db.transaction()

    #     @firestore.transactional
    #     def set_category(trans, purchase, category) -> bool:
    #         try:
    #             categories = self.db.collection("categories_purchases")
    #             if categories.document(category).get():
    #                 purchases = categories.document(category).get().to_dict().get("purchase")
                
    #             return True
    #         except Exception as err:
    #             print(err)
    #             return False

    #     return set_category(transaction, purchase, category)
    
    def get_purchase_categories(self) -> dict:
        """
            Get set of categories, automatically assigned to some purchases
        """

        transaction = self.db.transaction()

        @firestore.transactional
        def get_categories(trans) -> dict:
            try:
                result = {}

                categories = self.db.collection("purchases_categories").get()


                for category in categories:
                    for item in category._data["items"]:
                        result[item] = category.id
                return result
            except Exception as err:
                print(err)
                return {}
            
        return get_categories(transaction)
