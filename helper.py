import random
import string

import allure
import requests

from data import Url


class Helper:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def generate_registration_data():
        email = Helper.generate_random_string(10) + '@yandex.ru'
        password = Helper.generate_random_string(10)
        name = Helper.generate_random_string(10)

        registration_data = {
            "email": email,
            "password": password,
            "name": name
        }
        return registration_data


class User:
    @staticmethod
    @allure.step("Зарегистрировать нового пользователя")
    def register_new_user_and_return_response(payload):
        response = requests.post(Url.URL + Url.REGISTER_USER_HANDLE, data=payload)
        return response

    @staticmethod
    def delete_user_and_return_response(token, email):
        response = requests.delete(Url.URL + Url.AUTHORIZATION_USER_HANDLE,
                                   headers={'Authorization': token},
                                   data={"email": email})
        return response

    @staticmethod
    @allure.step("Сделать авторизацию пользователя")
    def login_user_and_return_response(email, password):
        response = requests.post(Url.URL + Url.LOGIN_USER_HANDLE,
                                 data={"email": email, "password": password}
                                 )
        return response

    @staticmethod
    @allure.step("Изменить данные пользователя")
    def change_user_data_and_return_response(token, field_to_change, new_data):
        response = requests.patch(Url.URL + Url.AUTHORIZATION_USER_HANDLE,
                                  headers={'Authorization': token},
                                  data={field_to_change: new_data})
        return response


class Order:
    @staticmethod
    @allure.step("Создать заказ для авторизованного пользователя")
    def create_order_with_auth_and_return_response(token, ingredient_list):
        response = requests.post(Url.URL + Url.ORDERS_HANDLE,
                                 headers={'Authorization': token},
                                 data={"ingredients": ingredient_list})
        return response

    @staticmethod
    @allure.step("Создать заказ без авторизации")
    def create_order_without_auth_and_return_response(ingredient_list):
        response = requests.post(Url.URL + Url.ORDERS_HANDLE,
                                 data={"ingredients": ingredient_list})
        return response

    @staticmethod
    @allure.step("Получить список заказов")
    def get_orders(token):
        response = requests.get(Url.URL + Url.ORDERS_HANDLE,
                                headers={'Authorization': token})
        return response
