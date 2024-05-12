import allure
import requests

from data import Ingredients, Url, Message
from helper import Helper, User, Order


class TestGetOrders:
    payload = None
    registration_response = None

    @classmethod
    def setup_class(cls):
        cls.payload = Helper.generate_registration_data()
        cls.registration_response = User.register_new_user_and_return_response(cls.payload)

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description('На корректный запрос на получение заказов авторизованного пользователя '
                        'получаем ответ с кодом 200. '
                        'В теле ответа длина массива "orders" равно количеству раннее созданных заказов')
    def test_get_orders_authorized_user_success(self):
        ingredient_list_1 = [Ingredients.FLUORESCENT_BUN,
                             Ingredients.IMMORTAL_PROTOSTOMIA_MEAT,
                             Ingredients.SPACE_SAUCE]
        ingredient_list_2 = [Ingredients.KRATOR_BUN,
                             Ingredients.BEEF_METEORITE,
                             Ingredients.TRADITIONAL_GALACTIC_SAUCE]
        Order.create_order_with_auth_and_return_response(
            self.registration_response.json()['accessToken'], ingredient_list_1)
        Order.create_order_with_auth_and_return_response(
            self.registration_response.json()['accessToken'], ingredient_list_2)

        response = Order.get_orders(self.registration_response.json()['accessToken'])
        assert response.status_code == 200 and len(response.json()["orders"]) == 2

    @allure.title("Нельзя получить список заказов без авторизации пользователя")
    @allure.description('На запрос без авторизации пользователя на получение заказов  '
                        'получаем ответ с кодом 401. '
                        'В теле ответа есть сообщение "You should be authorised"')
    def test_get_orders_unauthorized(self):
        response = requests.get(Url.URL + Url.ORDERS_HANDLE)
        assert response.status_code == 401 and response.json()["message"] == Message.SHOULD_AUTHORISED

    @classmethod
    def teardown_class(cls):
        User.delete_user_and_return_response(cls.registration_response.json()['accessToken'], cls.payload['email'])
