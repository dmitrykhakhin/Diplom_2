import allure

from data import Ingredients, Message
from helper import Helper, User, Order


class TestCreateOrder:
    payload = None
    registration_response = None

    @classmethod
    def setup_class(cls):
        cls.payload = Helper.generate_registration_data()
        cls.registration_response = User.register_new_user_and_return_response(cls.payload)

    @allure.title("Успешное создание заказа авторизованным пользователем")
    @allure.description('На корректный запрос на создание заказа авторизованным пользователем '
                        'получаем ответ с кодом 200, в теле ответа содержится название созданного бургера '
                        'и email пользователя')
    def test_create_order_with_authorization_success(self):
        ingredient_list = [Ingredients.FLUORESCENT_BUN,
                           Ingredients.IMMORTAL_PROTOSTOMIA_MEAT,
                           Ingredients.SPACE_SAUCE]
        response = Order.create_order_with_auth_and_return_response(
            self.registration_response.json()['accessToken'],
            ingredient_list
        )
        assert (response.status_code == 200
                and response.json()["name"] == "Space бессмертный флюоресцентный бургер"
                and response.json()["order"]["owner"]["email"] == self.payload["email"])

    @allure.title("Успешное создание заказа без авторизации пользователя")
    @allure.description('На корректный запрос на создание заказа без авторизации пользователя'
                        'получаем ответ с кодом 200, в теле ответа содержится название созданного бургера')
    def test_create_order_without_authorization_success(self):
        ingredient_list = [Ingredients.FLUORESCENT_BUN,
                           Ingredients.IMMORTAL_PROTOSTOMIA_MEAT,
                           Ingredients.SPACE_SAUCE]
        response = Order.create_order_without_auth_and_return_response(ingredient_list)
        assert response.status_code == 200 and response.json()["name"] == "Space бессмертный флюоресцентный бургер"

    @allure.title("Нельзя создать заказа без ингредиентов")
    @allure.description('При попытке создать заказ без ингредиентов получаем ответ с кодом 400 '
                        'и в теле ответа есть сообщение "Ingredient ids must be provided"')
    def test_create_order_no_ingredients_bad_request(self):
        ingredient_list = []
        response = Order.create_order_without_auth_and_return_response(ingredient_list)
        assert response.status_code == 400 and response.json()["message"] == Message.INGREDIENTS_MUST_PROVIDED

    @allure.title("Нельзя создать заказ c некорректным хэшем ингредиента")
    @allure.description('При попытке создать заказ c некорректным хэшем ингредиента получаем ответ с кодом 500 '
                        'и в теле ответа есть тэг "<pre>Internal Server Error</pre>"')
    def test_create_order_incorrect_ingredient_hash_server_error(self):
        incorrect_ingredient_hash = Helper.generate_random_string(24)
        ingredient_list = [incorrect_ingredient_hash,
                           Ingredients.IMMORTAL_PROTOSTOMIA_MEAT,
                           Ingredients.SPACE_SAUCE]
        response = Order.create_order_without_auth_and_return_response(ingredient_list)
        assert response.status_code == 500 and "<pre>Internal Server Error</pre>" in str(response.content)

    @classmethod
    def teardown_class(cls):
        User.delete_user_and_return_response(cls.registration_response.json()['accessToken'], cls.payload['email'])
