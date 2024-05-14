import allure

from data import Message
from helper import Helper, User


class TestLoginUser:
    payload = None
    registration_response = None

    @classmethod
    def setup_class(cls):
        cls.payload = Helper.generate_registration_data()
        cls.registration_response = User.register_new_user_and_return_response(cls.payload)

    @allure.title("Успешный логин под существующим пользователем")
    @allure.description('На корректный запрос для логина под существующим пользователем получаем ответ с кодом 200'
                        ' и в body есть accessToken')
    def test_login_user_correct_request_success(self):
        login_response = User.login_user_and_return_response(self.payload['email'], self.payload['password'])
        assert login_response.status_code == 200 and 'accessToken' in login_response.json()

    @allure.title("Запрет логина при вводе некорректного email")
    @allure.description('На запрос для логина c некорректным email получаем ответ с кодом 401'
                        ' и сообщением "email or password are incorrect"')
    def test_login_user_incorrect_email_unauthorized(self):
        incorrect_email = Helper.generate_random_string(10) + '@yandex.ru'
        login_response = User.login_user_and_return_response(incorrect_email, self.payload['password'])
        assert login_response.status_code == 401 and login_response.json()["message"] == Message.INCORRECT_DATA

    @allure.title("Запрет логина при вводе некорректного пароля")
    @allure.description('На запрос для логина c некорректным паролем получаем ответ с кодом 401'
                        ' и сообщением "email or password are incorrect"')
    def test_login_user_incorrect_password_unauthorized(self):
        incorrect_password = Helper.generate_random_string(10)
        login_response = User.login_user_and_return_response(self.payload['email'], incorrect_password)
        assert login_response.status_code == 401 and login_response.json()["message"] == Message.INCORRECT_DATA

    @classmethod
    def teardown_class(cls):
        User.delete_user_and_return_response(cls.registration_response.json()['accessToken'], cls.payload['email'])
