import allure
import requests

from data import Url, Message
from helper import Helper, User


class TestChangeUserData:
    payload = None
    registration_response = None

    @classmethod
    def setup_class(cls):
        cls.payload = Helper.generate_registration_data()
        cls.registration_response = User.register_new_user_and_return_response(cls.payload)

    @allure.title("Успешное изменение email пользователя")
    @allure.description('На корректный запрос изменение email пользователя получаем ответ с кодом 200'
                        ' и body содержит новый email и старое значение поля name')
    def test_change_user_data_new_email_success(self):
        access_token = self.registration_response.json()['accessToken']
        self.payload['email'] = Helper.generate_random_string(10) + '@yandex.ru'
        change_user_data_response = User.change_user_data_and_return_response(access_token,
                                                                              "email",
                                                                              self.payload['email'])
        assert (change_user_data_response.status_code == 200
                and change_user_data_response.json()["user"] == {"email": self.payload['email'],
                                                                 "name": self.payload['name']}
                )

    @allure.title("Успешное изменение поля name пользователя")
    @allure.description('На корректный запрос изменение email пользователя получаем ответ с кодом 200'
                        ' и body содержит новое значение поля name и старый email')
    def test_change_user_data_new_name_success(self):
        access_token = self.registration_response.json()['accessToken']
        self.payload['name'] = Helper.generate_random_string(10)
        change_user_data_response = User.change_user_data_and_return_response(access_token,
                                                                              "name",
                                                                              self.payload['name'])
        assert (change_user_data_response.status_code == 200
                and change_user_data_response.json()["user"] == {"email": self.payload['email'],
                                                                 "name": self.payload['name']}
                )

    @allure.title("Успешное изменение поля password пользователя и успешный логин с новым паролем")
    @allure.description('На корректный запрос на изменение пароля пользователя получаем ответ с кодом 200'
                        ' и в теле ответа есть email и имя пользователя'
                        ' и логин пользователя с новым паролем возвращает код 200'
                        ' и тело ответа содержит ""success: true""')
    def test_change_user_data_new_password_successful_login(self):
        access_token = self.registration_response.json()['accessToken']
        self.payload['password'] = Helper.generate_random_string(10)
        change_user_data_response = User.change_user_data_and_return_response(access_token,
                                                                              "password",
                                                                              self.payload['password'])
        login_response = User.login_user_and_return_response(self.payload['email'], self.payload['password'])
        assert (change_user_data_response.status_code == 200
                and change_user_data_response.json()["user"] == {"email": self.payload['email'],
                                                                 "name": self.payload['name']}
                and login_response.status_code == 200 and login_response.json()['success'] is True)

    @allure.title("Нельзя изменить данные без авторизации")
    @allure.description('На запрос на изменение поля email без авторизации получаем ответ с кодом 401'
                        ' и в теле ответа есть сообщение "You should be authorised"')
    def test_change_user_data_new_mail_without_auth_unsuccessful(self):
        new_mail = Helper.generate_random_string(10) + '@yandex.ru'
        response = requests.patch(Url.URL + Url.AUTHORIZATION_USER_HANDLE,
                                  data={f"mail": new_mail})
        assert response.status_code == 401 and response.json()["message"] == Message.SHOULD_AUTHORISED

    @classmethod
    def teardown_class(cls):
        User.delete_user_and_return_response(cls.registration_response.json()['accessToken'], cls.payload['email'])
