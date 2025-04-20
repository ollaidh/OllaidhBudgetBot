import os
import unittest

import requests

import threading

from db_adapters.firestore_adapter import FirestoreAdapter
from db_adapters.adapter import PurchaseInfo
from unittest.mock import patch


def test_setUp() -> None:
    emulator_host = os.getenv("FIRESTORE_EMULATOR_HOST")
    assert emulator_host is not None
    project_id = os.getenv("BUDBOT_PROJECT_ID")
    assert project_id is not None
    url = f"http://{emulator_host}/emulator/v1/projects/{project_id}/databases/(default)/documents"
    response = requests.delete(url)
    assert response.status_code == 200


@patch("db_adapters.firestore_adapter.get_month_today")
@patch("db_adapters.firestore_adapter.get_date_today")
def test_add_purchase(date_mock, month_mock):
    adapter = FirestoreAdapter()

    month_mock.return_value = "2022-10"
    date_mock.return_value = "2022-10-04"
    success = adapter.add_purchase(PurchaseInfo("coffee", 3, "takeaway"))
    assert success is True

    purch1 = (
        adapter.db.collection("months")
        .document(month_mock())
        .collection("items")
        .document("0")
        .get()
        .to_dict()
    )
    assert {
        "purchase": "coffee",
        "price": 3,
        "category": "takeaway",
        "date": date_mock(),
    } == purch1

    month_mock.return_value = "2022-12"
    date_mock.return_value = "2022-12-31"
    success = adapter.add_purchase(PurchaseInfo("bulka", 4, "bread"))
    assert success is True

    purch2 = (
        adapter.db.collection("months")
        .document(month_mock())
        .collection("items")
        .document("0")
        .get()
        .to_dict()
    )
    assert purch2 == {
        "purchase": "bulka",
        "price": 4,
        "category": "bread",
        "date": date_mock(),
    }

    success = adapter.add_purchase(PurchaseInfo("poop bag", 1, "dog"))
    assert success is True
    purch3 = (
        adapter.db.collection("months")
        .document(month_mock())
        .collection("items")
        .document("1")
        .get()
        .to_dict()
    )
    assert purch3 == {
        "purchase": "poop bag",
        "price": 1,
        "category": "dog",
        "date": date_mock(),
    }


@patch("db_adapters.firestore_adapter.get_month_today")
@patch("db_adapters.firestore_adapter.get_date_today")
def test_add_purchase_race_condition(date_mock, month_mock):
    barrier = threading.Barrier(3)
    adapter = FirestoreAdapter(sleep_wait_ms=1000)

    def add_purchase_coffee():
        barrier.wait()
        month_mock.return_value = "2000-04"
        date_mock.return_value = "2000-04-01"
        adapter.add_purchase(PurchaseInfo("thread_coffee", 1, "thread_coffee"))

    def add_purchase_tea():
        barrier.wait()
        month_mock.return_value = "2000-05"
        date_mock.return_value = "2000-05-02"
        adapter.add_purchase(PurchaseInfo("thread_tea", 2, "thread_tea"))

    month_mock.return_value = "2000-01"
    date_mock.return_value = "2000-01-01"
    success = adapter.add_purchase(PurchaseInfo("coffee", 3, "takeaway"))
    assert success is True

    assert {"TOTAL": 3, "takeaway": 3} == adapter.calculate_spent(
        "2000-01", "2000-02", "$each"
    )

    month_mock.return_value = "2000-02"
    date_mock.return_value = "2000-02-15"
    adapter.add_purchase(PurchaseInfo("bulka", 4, "bread"))

    assert {"TOTAL": 7, "bread": 4, "takeaway": 3} == adapter.calculate_spent(
        "2000-01", "2000-03", "$each"
    )

    buy_coffee = threading.Thread(target=add_purchase_coffee)
    buy_coffee.start()

    buy_tea = threading.Thread(target=add_purchase_tea)
    buy_tea.start()

    barrier.wait()

    buy_coffee.join()
    buy_tea.join()

    assert {
        "TOTAL": 10,
        "bread": 4,
        "takeaway": 3,
        "thread_coffee": 1,
        "thread_tea": 2,
    } == adapter.calculate_spent("2000-01", "2000-05", "$each")


@patch("db_adapters.firestore_adapter.get_month_today")
def test_spent(date_mock):
    adapter = FirestoreAdapter()
    date_mock.return_value = "2023-01"
    adapter.add_purchase(PurchaseInfo("proplan", 20, "dog"))
    date_mock.return_value = "2023-01"
    adapter.add_purchase(PurchaseInfo("baguette", 1.5, "bread"))
    adapter.add_purchase(PurchaseInfo("muffin", 2, "takeaway"))
    date_mock.return_value = "2023-02"
    adapter.add_purchase(PurchaseInfo("pizza", 12.5, "takeaway"))

    spent_result = adapter.calculate_spent("2023-01", "2023-02", "takeaway")
    assert isinstance(spent_result, dict) is True
    assert list(spent_result.items()) == [
        ("TAKEAWAY", 14.5),
        ("pizza", 12.5),
        ("muffin", 2),
    ]

    spent_result = adapter.calculate_spent("2023-01", "2023-01", "$all")
    assert spent_result == {"$all": 23.5}

    spent_result = adapter.calculate_spent("2023-01", "2023-02", "$each")
    assert isinstance(spent_result, dict) is True
    assert [("TOTAL", 36.0), ("dog", 20), ("takeaway", 14.5), ("bread", 1.5)] == list(
        spent_result.items()
    )

    spent_result = adapter.calculate_spent("2028-01", "2029-02", "")
    assert spent_result == {}

    spent_result = adapter.calculate_spent("2028-01", "2029-02", "takeaway")
    assert spent_result == {}

    spent_result = adapter.calculate_spent("2028-01", "2029-02", "$all")
    assert spent_result == {}

    spent_result = adapter.calculate_spent("2023-01", "2023-02", "gagagagaga")
    assert spent_result == {}


@patch("db_adapters.firestore_adapter.get_month_today")
def test_set_month_limit(date_mock):
    adapter = FirestoreAdapter()
    date_mock.return_value = "2025-03"
    adapter.set_month_limit(2000)
