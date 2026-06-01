"""Билдеры тестовых данных.

Генерируем валидный payload с возможностью переопределить любое поле —
так тесты остаются независимыми и не делят между собой состояние.
"""
import random
from datetime import date, timedelta


def valid_booking(**overrides) -> dict:
    checkin = date.today()
    checkout = checkin + timedelta(days=random.randint(1, 14))
    payload = {
        "firstname": "Rodion",
        "lastname": "Test",
        "totalprice": random.randint(50, 1000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        },
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload
