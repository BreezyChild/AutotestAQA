import allure

from helpers.booking_payloads import valid_booking


@allure.feature("Delete Booking")
class TestDeleteBooking:
    @allure.title("DELETE удаляет бронь (201), после чего GET даёт 404")
    def test_delete_booking(self, api, auth_token):
        booking_id = api.create_booking(valid_booking()).json()["bookingid"]

        delete_response = api.delete_booking(booking_id, auth_token)
        assert delete_response.status_code == 201  # известная особенность API

        get_response = api.get_booking(booking_id)
        assert get_response.status_code == 404

    @allure.title("DELETE без токена запрещён (403)")
    def test_delete_without_token_forbidden(self, api):
        booking_id = api.create_booking(valid_booking()).json()["bookingid"]
        response = api.delete_booking(booking_id, token="")
        assert response.status_code == 403
