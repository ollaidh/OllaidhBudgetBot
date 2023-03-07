import os

from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client
from typing import Optional
from date_utils import get_date_today
from date_utils import months_spent
from db_adapters.adapter import PurchaseInfo


# TODO: transactions!
class FirestoreAdapter:
    def __init__(self):
        project_id = os.getenv('BUDBOT_PROJECT_ID')
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is None:
            cred = AnonymousCredentials()
        else:
            cred = None
        self.db = Client(project=project_id, credentials=cred)
        # self.date = str(datetime.date.today())[:-3]

    def add_purchase(self, purchase: PurchaseInfo) -> bool:
        try:
            month_database = self.db.collection("months").document(get_date_today())
            data = month_database.get().to_dict()
            if data:
                last_id = int(data['last_id'])
                last_id += 1
            else:
                month_database.set({'last_id': "0"})
                last_id = 0

            self.db.collection("months").document(get_date_today()).update({'last_id': str(last_id)})

            curr_purchase = self.db.collection("months").document(get_date_today()).collection("items").document(str(last_id))
            curr_purchase.set(
                {
                    "purchase": purchase.name,
                    "price": purchase.price,
                    "category": purchase.category,
                    "date": get_date_today()
                }
            )
            return True
        except Exception as err:
            print(err)
            return False

    def delete_purchase(self) -> bool:
        try:
            last_id = self.db.collection("months").document(get_date_today()).get().to_dict()['last_id']
            if last_id:
                self.db.collection("months").document(get_date_today()).collection('items').document(str(last_id)).delete()
                self.db.collection("months").document(get_date_today()).update({'last_id': str(int(last_id) - 1)})
            return True
        except:
            return False

    def calculate_spent(self, start_date: str, end_date: str, category: str) -> Optional[dict]:
        try:
            months = months_spent(start_date, end_date)
            spent = {}

            def add_to_spent(cat, price):
                spent[cat] = spent.get(cat, 0) + price

            for month in months:
                items = self.db.collection("months").document(month).collection("items").get()
                if not items:
                    continue
                for item in items:
                    if category not in [item.to_dict()["category"], '$all', '$each']:
                        continue
                    if category == '$all':
                        add_to_spent(category, item.to_dict()["price"])
                    else:
                        add_to_spent(item.to_dict()["category"], item.to_dict()["price"])
            return spent
        except:
            return None




