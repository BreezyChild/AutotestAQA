import allure


@allure.feature("Get Booking")
class TestGetBooking:
    @allure.title("GET /booking возвращает список идентификаторов")
    def test_get_all_booking_ids(self, api):
        response = api.get_booking_ids()
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "bookingid" in data[0]

    @allure.title("GET существующей брони возвращает корректные данные")
    def test_get_existing_booking(self, api, created_booking):
        booking_id, payload = created_booking
        response = api.get_booking(booking_id)
        assert response.status_code == 200
        body = response.json()
        assert body["firstname"] == payload["firstname"]
        assert body["lastname"] == payload["lastname"]

    @allure.title("GET несуществующей брони возвращает 404")
    def test_get_nonexistent_booking(self, api):
        response = api.get_booking(99999999)
        assert response.status_code == 404
