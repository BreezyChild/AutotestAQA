import allure
import pytest

from config import AUTH_PASSWORD, AUTH_USERNAME


@allure.feature("Auth")
class TestAuth:
    @allure.title("Валидные креды возвращают токен")
    @pytest.mark.smoke
    def test_valid_credentials_return_token(self, api):
        response = api.create_token(AUTH_USERNAME, AUTH_PASSWORD)
        assert response.status_code == 200
        body = response.json()
        assert "token" in body
        assert isinstance(body["token"], str) and body["token"]

    @allure.title("Невалидные креды не возвращают токен")
    @pytest.mark.parametrize(
        "username,password",
        [
            ("admin", "wrong_password"),
            ("wrong_user", "password123"),
            ("", ""),
        ],
    )
    def test_invalid_credentials_no_token(self, api, username, password):
        response = api.create_token(username, password)
        # API отвечает 200 даже при ошибке — токена в теле нет
        assert response.status_code == 200
        assert "token" not in response.json()
        assert response.json().get("reason") == "Bad credentials"
