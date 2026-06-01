"""Конфигурация тестового прогона.

Все значения можно переопределить переменными окружения,
что удобно для запуска против разных стендов (dev/stage) и в CI.
"""
import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "password123")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30"))
