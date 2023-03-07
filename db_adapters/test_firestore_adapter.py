import os
import unittest

import requests

from db_adapters.firestore_adapter import FirestoreAdapter
from db_adapters.adapter import PurchaseInfo
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        emulator_host = os.getenv('FIRESTORE_EMULATOR_HOST')
        project_id = os.getenv('BUDBOT_PROJECT_ID')
        url = f'http://{emulator_host}/emulator/v1/projects/{project_id}/databases/(default)/documents'
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)

    @patch('db_adapters.firestore_adapter.get_date_today')
    def test_add_purchase(self, date_mock):
        adapter = FirestoreAdapter()

        date_mock.return_value = "2022-10"
        success = adapter.add_purchase(PurchaseInfo("coffee", 3, "takeaway"))
        self.assertTrue(success)

        purch1 = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "0").get().to_dict()
        self.assertEqual(
            {
                "purchase": "coffee",
                "price": 3,
                "category": "takeaway",
                "date": date_mock()
            },
            purch1
        )

        date_mock.return_value = "2022-12"
        success = adapter.add_purchase(PurchaseInfo("bulka", 4, "bread"))
        self.assertTrue(success)

        purch2 = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "0").get().to_dict()
        self.assertEqual(purch2, {
            "purchase": "bulka",
            "price": 4,
            "category": "bread",
            "date": date_mock()
        })

        success = adapter.add_purchase(PurchaseInfo("poop bag", 1, "dog"))
        self.assertTrue(success)
        purch3 = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "1").get().to_dict()
        self.assertEqual(purch3, {
            "purchase": "poop bag",
            "price": 1,
            "category": "dog",
            "date": date_mock()
        })

    @patch('db_adapters.firestore_adapter.get_date_today')
    def test_delete_purchase(self, date_mock):
        adapter = FirestoreAdapter()
        date_mock.return_value = "2022-12"
        adapter.add_purchase(PurchaseInfo("bulka", 4, "bread"))
        adapter.add_purchase(PurchaseInfo("croissant", 3, "takeaway"))
        success = adapter.delete_purchase()
        self.assertTrue(success)
        deleted_purchase = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "1").get()
        self.assertFalse(deleted_purchase.exists)
        last_purchase = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "0").get().to_dict()
        self.assertEqual(last_purchase, {
            "purchase": "bulka",
            "price": 4,
            "category": "bread",
            "date": "2022-12"
        })

    @patch('db_adapters.firestore_adapter.get_date_today')
    def test_spent(self, date_mock):
        adapter = FirestoreAdapter()
        date_mock.return_value = "2023-01"
        adapter.add_purchase(PurchaseInfo("proplan", 20, "dog"))
        date_mock.return_value = "2023-01"
        adapter.add_purchase(PurchaseInfo("baguette", 1.5, "bread"))
        adapter.add_purchase(PurchaseInfo("muffin", 2, "takeaway"))
        date_mock.return_value = "2023-02"
        adapter.add_purchase(PurchaseInfo("pizza", 12.5, "takeaway"))
        spent_result = adapter.calculate_spent("2023-01", "2023-02", "takeaway")
        self.assertEqual(spent_result, {"$all": 36.0, "takeaway": 14.5})
        spent_result = adapter.calculate_spent("2023-01", "2023-01", "$all")
        self.assertEqual(spent_result, {"$all": 23.5})
        spent_result = adapter.calculate_spent("2023-01", "2023-02", "$each")
        self.assertEqual(spent_result, {"$all": 36.0, "takeaway": 14.5, "bread": 1.5, "dog": 20.0})


if __name__ == '__main__':
    unittest.main()
