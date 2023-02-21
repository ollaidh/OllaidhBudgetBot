import os

from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client
from typing import Optional
from date_utils import get_date_today

# TODO: transactions!
class FirestoreAdapter:
    def __init__(self):
        cred = AnonymousCredentials()
        project_id = os.getenv('BUDBOT_PROJECT_ID')
        self.db = Client(project=project_id, credentials=cred)
        # self.date = str(datetime.date.today())[:-3]

    def add_purchase(self, purchase: str, price: str, category: str):
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
                    "purchase": purchase,
                    "price": price,
                    "category": category,
                    "date": get_date_today()
                }
            )
            return True
        except Exception as err:
            print(err)
            return False

    def delete_purchase(self):
        try:
            last_id = self.db.collection("months").document(get_date_today()).get().to_dict()['last_id']
            if last_id:
                self.db.collection("months").document(get_date_today()).collection('items').document(str(last_id)).delete()
                self.db.collection("months").document(get_date_today()).update({'last_id': str(int(last_id) - 1)})
            return True
        except:
            return False

    def months_spent(self, start_date: str, end_date: str):
        start_year = start_date[:4]
        end_year = end_date[:4]
        start_month = start_date[5:]
        end_month = end_date[5:]
        if end_year > start_year:
            months = [start_year + '-' + str(i).zfill(2) for i in range(int(start_month), 13)] + [
                end_year + '-' + str(i).zfill(2) for i in range(1, int(end_month) + 1)]
        else:
            months = [start_year + '-' + str(i).zfill(2) for i in range(int(start_month), int(end_month) + 1)]
        return months

    def calculate_spent(self, start_date: str, end_date: str, category: str) -> Optional[dict]:
        try:
            months = self.months_spent(start_date, end_date)
            spent = {}
            if category != "$each":
                spent[category] = 0

            for month in months:
                items = self.db.collection("months").document(month).collection("items").get()
                if items:
                    for item in items:
                        if category == '$all' or item.to_dict()["category"] == category:
                            spent[category] += float(item.to_dict()["price"])
                        if category == '$each':
                            if item.to_dict()["category"] not in spent.keys():
                                spent[item.to_dict()["category"]] = 0
                            spent[item.to_dict()["category"]] += float(item.to_dict()["price"])
            return spent
        except:
            return None



