import allure

from data import Message
from helper import Helper, User


class TestCreateUser:
    payload = None
    response = None

    @classmethod
    def setup_class(cls):
        cls.payload = Helper.generate_registration_data()
        cls.response = User.register_new_user_and_return_response(cls.payload)

    @allure.title("Успешное создание пользователя")
    @allure.description('На корректный запрос для создания пользователя получаем ответ с кодом 200'
                        ' и в body есть {"success": true}')
    def test_create_user_correct_request_success(self):
        assert self.response.status_code == 200 and self.response.json()['success'] is True

    @allure.title("Невозможно создать пользователя, который уже зарегистрирован")
    @allure.description('При попытке создать пользователя, который уже зарегистрирован, получаем ответ с кодом 403'
                        ' и в body есть сообщение "User already exists"')
    def test_create_user_already_registered_forbidden(self):
        self.response = User.register_new_user_and_return_response(self.payload)
        assert self.response.status_code == 403 and self.response.json()['message'] == Message.USER_ALREADY_EXISTS

    @allure.title("Невозможно создать пользователя с пустым полем email")
    @allure.description('При попытке создать пользователя с пустым полем email получаем ответ с кодом 403'
                        ' и в body есть сообщение "Email, password and name are required fields"')
    def test_create_user_empty_email_forbidden(self):
        payload_with_empty_email = Helper.generate_registration_data()
        payload_with_empty_email["email"] = ""
        response = User.register_new_user_and_return_response(payload_with_empty_email)
        assert response.status_code == 403 and response.json()['message'] == Message.REQUIRED_FIELDS

    @allure.title("Невозможно создать пользователя с пустым полем password")
    @allure.description('При попытке создать пользователя с пустым полем password получаем ответ с кодом 403'
                        ' и в body есть сообщение "Email, password and name are required fields"')
    def test_create_user_empty_password_forbidden(self):
        payload_with_empty_email = Helper.generate_registration_data()
        payload_with_empty_email["password"] = ""
        response = User.register_new_user_and_return_response(payload_with_empty_email)
        assert response.status_code == 403 and response.json()['message'] == Message.REQUIRED_FIELDS

    @allure.title("Невозможно создать пользователя с пустым полем name")
    @allure.description('При попытке создать пользователя с пустым полем password получаем ответ с кодом 403'
                        ' и в body есть сообщение "Email, password and name are required fields"')
    def test_create_user_empty_name_forbidden(self):
        payload_with_empty_email = Helper.generate_registration_data()
        payload_with_empty_email["name"] = ""
        response = User.register_new_user_and_return_response(payload_with_empty_email)
        assert response.status_code == 403 and response.json()['message'] == Message.REQUIRED_FIELDS

    @classmethod
    def teardown_class(cls):
        User.delete_user_and_return_response(cls.response.json()['accessToken'], cls.payload['email'])
