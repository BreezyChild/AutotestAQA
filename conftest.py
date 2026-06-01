"""Общие фикстуры pytest.

- session: один requests.Session на весь прогон (переиспользование соединений)
- api: экземпляр клиента BookingAPI
- auth_token: валидный токен авторизации
- created_booking: создаёт бронь перед тестом и удаляет её после (teardown),
  чтобы тесты не оставляли мусор на стенде
"""
import pytest
import requests

from config import AUTH_PASSWORD, AUTH_USERNAME
from helpers.api_client import BookingAPI
from helpers.booking_payloads import valid_booking


@pytest.fixture(scope="session")
def session() -> requests.Session:
    s = requests.Session()
    yield s
    s.close()


@pytest.fixture()
def api(session) -> BookingAPI:
    return BookingAPI(session=session)


@pytest.fixture()
def auth_token(api) -> str:
    response = api.create_token(AUTH_USERNAME, AUTH_PASSWORD)
    assert response.status_code == 200, "Не удалось получить токен авторизации"
    token = response.json().get("token")
    assert token, "В ответе /auth отсутствует token"
    return token


@pytest.fixture()
def created_booking(api):
    payload = valid_booking()
    response = api.create_booking(payload)
    assert response.status_code == 200, "Не удалось создать бронь для теста"
    booking_id = response.json()["bookingid"]

    yield booking_id, payload

    # teardown: подчищаем за собой, ошибки очистки не валят тест
    try:
        token = api.create_token(AUTH_USERNAME, AUTH_PASSWORD).json().get("token")
        if token:
            api.delete_booking(booking_id, token)
    except Exception:
        pass
