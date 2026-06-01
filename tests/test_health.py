import allure
import pytest


@allure.feature("Health")
@allure.title("GET /ping возвращает 201 Created")
@pytest.mark.smoke
def test_health_check(api):
    response = api.health_check()
    assert response.status_code == 201
