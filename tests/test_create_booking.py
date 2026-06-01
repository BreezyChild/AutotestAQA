import allure
from jsonschema import validate

from helpers.booking_payloads import valid_booking
from schemas.booking_schema import CREATE_BOOKING_SCHEMA


@allure.feature("Create Booking")
class TestCreateBooking:
    @allure.title("Создание брони возвращает 200 и тело по схеме")
    def test_create_booking_success(self, api):
        payload = valid_booking(firstname="Anna", lastname="Smith")
        response = api.create_booking(payload)

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=CREATE_BOOKING_SCHEMA)
        assert isinstance(body["bookingid"], int)
        assert body["booking"]["firstname"] == "Anna"
        assert body["booking"]["lastname"] == "Smith"

    @allure.title("Созданная бронь доступна по GET")
    def test_created_booking_is_retrievable(self, api):
        payload = valid_booking()
        booking_id = api.create_booking(payload).json()["bookingid"]

        response = api.get_booking(booking_id)
        assert response.status_code == 200
        assert response.json()["firstname"] == payload["firstname"]

    @allure.title("Создание без обязательных полей: фактически 500 (потенциальный баг)")
    def test_create_booking_missing_fields(self, api):
        response = api.create_booking({"firstname": "OnlyName"})
        # Ожидаемое по-хорошему — 400 Bad Request. API отдаёт 500 —
        # фиксируем фактическое поведение; в реальном проекте это баг-репорт.
        assert response.status_code == 500
