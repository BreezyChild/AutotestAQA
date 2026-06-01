"""Тонкий клиент над API Restful-Booker.

Service-object паттерн (API-аналог Page Object): тесты не работают
с requests напрямую, а вызывают понятные методы клиента. Это
изолирует знание об эндпоинтах в одном месте и делает тесты читаемыми.
"""
from typing import Optional

import requests

from config import BASE_URL, DEFAULT_TIMEOUT


class BookingAPI:
    def __init__(self, base_url: str = BASE_URL, session: Optional[requests.Session] = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def health_check(self) -> requests.Response:
        return self.session.get(self._url("/ping"), timeout=DEFAULT_TIMEOUT)

    def create_token(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            self._url("/auth"),
            json={"username": username, "password": password},
            timeout=DEFAULT_TIMEOUT,
        )

    def get_booking_ids(self, params: Optional[dict] = None) -> requests.Response:
        return self.session.get(
            self._url("/booking"),
            params=params,
            headers={"Accept": "application/json"},
            timeout=DEFAULT_TIMEOUT,
        )

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.session.get(
            self._url(f"/booking/{booking_id}"),
            headers={"Accept": "application/json"},
            timeout=DEFAULT_TIMEOUT,
        )

    def create_booking(self, payload: dict) -> requests.Response:
        return self.session.post(
            self._url("/booking"),
            json=payload,
            headers={"Accept": "application/json"},
            timeout=DEFAULT_TIMEOUT,
        )

    def update_booking(self, booking_id: int, payload: dict, token: str) -> requests.Response:
        return self.session.put(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers={"Accept": "application/json", "Cookie": f"token={token}"},
            timeout=DEFAULT_TIMEOUT,
        )

    def partial_update_booking(self, booking_id: int, payload: dict, token: str) -> requests.Response:
        return self.session.patch(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers={"Accept": "application/json", "Cookie": f"token={token}"},
            timeout=DEFAULT_TIMEOUT,
        )

    def delete_booking(self, booking_id: int, token: str) -> requests.Response:
        return self.session.delete(
            self._url(f"/booking/{booking_id}"),
            headers={"Cookie": f"token={token}"},
            timeout=DEFAULT_TIMEOUT,
        )
