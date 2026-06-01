import allure

from helpers.booking_payloads import valid_booking


@allure.feature("Update Booking")
class TestUpdateBooking:
    @allure.title("PUT полностью обновляет бронь")
    def test_full_update(self, api, auth_token, created_booking):
        booking_id, _ = created_booking
        new_payload = valid_booking(firstname="Updated", lastname="User", totalprice=777)

        response = api.update_booking(booking_id, new_payload, auth_token)
        assert response.status_code == 200
        body = response.json()
        assert body["firstname"] == "Updated"
        assert body["totalprice"] == 777

    @allure.title("PUT без токена запрещён (403)")
    def test_update_without_token_forbidden(self, api, created_booking):
        booking_id, _ = created_booking
        response = api.update_booking(booking_id, valid_booking(), token="")
        assert response.status_code == 403

    @allure.title("PATCH обновляет отдельное поле")
    def test_partial_update(self, api, auth_token, created_booking):
        booking_id, _ = created_booking
        response = api.partial_update_booking(booking_id, {"firstname": "Patched"}, auth_token)
        assert response.status_code == 200
        assert response.json()["firstname"] == "Patched"
