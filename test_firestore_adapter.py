import os
import unittest

import requests

from firestore_adapter import FirestoreAdapter
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        emulator_host = os.getenv('FIRESTORE_EMULATOR_HOST')
        project_id = os.getenv('BUDBOT_PROJECT_ID')
        url = f'http://{emulator_host}/emulator/v1/projects/{project_id}/databases/(default)/documents'
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)

    @patch('firestore_adapter.get_date_today')
    def test_add_purchase(self, date_mock):
        adapter = FirestoreAdapter()

        date_mock.return_value = "2022-10"
        success = adapter.add_purchase("coffee", "3", "takeaway")
        self.assertTrue(success)

        purch1 = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "0").get().to_dict()
        self.assertEqual(
            {
                "purchase": "coffee",
                "price": '3',
                "category": "takeaway",
                "date": date_mock()
            },
            purch1
        )

        date_mock.return_value = "2022-12"
        success = adapter.add_purchase("bulka", "4", "bread")
        self.assertTrue(success)

        purch2 = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "0").get().to_dict()
        self.assertEqual(purch2, {
            "purchase": "bulka",
            "price": '4',
            "category": "bread",
            "date": date_mock()
        })

        success = adapter.add_purchase("poop bag", "1", "dog")
        self.assertTrue(success)
        purch3 = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "1").get().to_dict()
        self.assertEqual(purch3, {
            "purchase": "poop bag",
            "price": '1',
            "category": "dog",
            "date": date_mock()
        })

    @patch('firestore_adapter.get_date_today')
    def test_delete_purchase(self, date_mock):
        adapter = FirestoreAdapter()
        date_mock.return_value = "2022-12"
        adapter.add_purchase("bulka", "4", "bread")
        adapter.add_purchase("croissant", "3", "takeaway")
        success = adapter.delete_purchase()
        self.assertTrue(success)
        deleted_purchase = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "1").get()
        self.assertFalse(deleted_purchase.exists)
        last_purchase = adapter.db.collection("months").document(date_mock()).collection("items").document(
            "0").get().to_dict()
        self.assertEqual(last_purchase, {
            "purchase": "bulka",
            "price": '4',
            "category": "bread",
            "date": "2022-12"
        })

    def test_months_spent(self):
        adapter = FirestoreAdapter()
        self.assertEqual(adapter.months_spent("2022-11", "2023-02"), ["2022-11", "2022-12", "2023-01", "2023-02"])
        self.assertEqual(adapter.months_spent("2022-05", "2022-08"), ["2022-05", "2022-06", "2022-07", "2022-08"])

    @patch('firestore_adapter.get_date_today')
    def test_spent(self, date_mock):
        adapter = FirestoreAdapter()
        date_mock.return_value = "2023-01"
        adapter.add_purchase("proplan", "20", "dog")
        date_mock.return_value = "2023-01"
        adapter.add_purchase("baguette", "1.5", "bread")
        adapter.add_purchase("muffin", "2", "takeaway")
        date_mock.return_value = "2023-02"
        adapter.add_purchase("pizza", "12.5", "takeaway")
        spent_result = adapter.calculate_spent("2023-01", "2023-02", "takeaway")
        self.assertEqual(spent_result, {"takeaway": 14.5})
        spent_result = adapter.calculate_spent("2023-01", "2023-01", "$all")
        self.assertEqual(spent_result, {"$all": 23.5})
        spent_result = adapter.calculate_spent("2023-01", "2023-02", "$each")
        self.assertEqual(spent_result, {"takeaway": 14.5, "bread": 1.5, "dog": 20.0})


if __name__ == '__main__':
    unittest.main()
